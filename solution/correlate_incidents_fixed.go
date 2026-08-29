// Stage two of the reference: the corrected incident-correlation engine.
//
// Every governing value is traced to its final dated entry in
// /app/incident/response_governance_log.md; triage_contract.json supplies the
// output contract only and no derivation rule.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"sort"
)

type event struct {
	EventID     string `json:"event_id"`
	Host        string `json:"host"`
	Account     string `json:"account"`
	Action      string `json:"action"`
	Sensor      string `json:"sensor"`
	ObservedTS  int64  `json:"observed_ts"`
	CorrectedTS int64  `json:"corrected_ts"`
	PID         int    `json:"pid"`
}

type policy struct {
	Default map[string]int64 `json:"default"`
}

type chainRow struct {
	ChainID    string   `json:"chain_id"`
	Account    string   `json:"account"`
	Hosts      []string `json:"hosts"`
	HostCount  int      `json:"host_count"`
	FirstTS    int64    `json:"first_ts"`
	LastTS     int64    `json:"last_ts"`
	EventCount int      `json:"event_count"`
	Severity   int64    `json:"severity"`
	Actions    []string `json:"actions"`
}

type queueRow struct {
	ChainID  string `json:"chain_id"`
	Account  string `json:"account"`
	Host     string `json:"host"`
	Severity int64  `json:"severity"`
	Reason   string `json:"reason"`
}

// #IR-5186: the severity the board fixed for each observed action. An action the
// table does not name contributes nothing.
var actionSeverity = map[string]int64{
	"logon":          5,
	"logon_failed":   8,
	"process_start":  10,
	"net_connect":    12,
	"file_write":     15,
	"share_mount":    20,
	"priv_escalate":  45,
	"log_cleared":    50,
}

func readJSON(path string, into any) {
	raw, err := os.ReadFile(path)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := json.Unmarshal(raw, into); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func writeJSON(path string, value any) {
	encoded, err := json.MarshalIndent(value, "", "  ")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := os.WriteFile(path, append(encoded, '\n'), 0o644); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

// The policy is read from its fixed absolute path, and any field the file omits
// keeps its governed baseline. A missing Go map key is zero, not the baseline,
// so the fallback has to be explicit.
func policyValue(pol policy, field string, baseline int64) int64 {
	if value, ok := pol.Default[field]; ok {
		return value
	}
	return baseline
}

func main() {
	input := flag.String("input", "/app/data/event_timeline.json", "recovered event timeline")
	outputDir := flag.String("output-dir", "/app/output", "output directory")
	flag.Parse()

	var events []event
	var pol policy
	// #IR-5150: the triage policy is always read from its fixed absolute path;
	// --input selects the timeline only.
	readJSON("/app/data/triage_policy.json", &pol)
	readJSON(*input, &events)

	sessionGap := policyValue(pol, "session_gap_sec", 1800)
	pivotMinHosts := int(policyValue(pol, "pivot_min_hosts", 3))
	severityFloor := policyValue(pol, "severity_floor", 40)
	chainWindow := policyValue(pol, "chain_window_sec", 7200)
	maxChainHosts := int(policyValue(pol, "max_chain_hosts", 12))

	// #IR-5182: every boundary in this procedure is drawn on the CORRECTED stamp,
	// never on the stamp the sensor recorded.
	sort.Slice(events, func(i, j int) bool {
		if events[i].CorrectedTS != events[j].CorrectedTS {
			return events[i].CorrectedTS < events[j].CorrectedTS
		}
		return events[i].EventID < events[j].EventID
	})

	byAccount := map[string][]event{}
	byHostAccount := map[string][]event{}
	hosts := map[string]bool{}
	for _, e := range events {
		byAccount[e.Account] = append(byAccount[e.Account], e)
		byHostAccount[e.Host+"\x00"+e.Account] = append(byHostAccount[e.Host+"\x00"+e.Account], e)
		hosts[e.Host] = true
	}

	// sessions are reported only as a count; a gap longer than the policy's
	// session_gap_sec opens a new session on that host for that account.
	sessionCount := 0
	for _, group := range byHostAccount {
		sessionCount++
		for i := 1; i < len(group); i++ {
			if group[i].CorrectedTS-group[i-1].CorrectedTS > sessionGap {
				sessionCount++
			}
		}
	}

	accounts := make([]string, 0, len(byAccount))
	for a := range byAccount {
		accounts = append(accounts, a)
	}
	sort.Strings(accounts)

	chains := make([]chainRow, 0)
	queue := make([]queueRow, 0)
	candidateCount, truncatedCount := 0, 0

	for _, account := range accounts {
		group := byAccount[account]
		start := 0
		for start < len(group) {
			// #IR-5190: a run closes when the next event lies further than
			// chain_window_sec from the one before it, so the window slides with the
			// activity rather than sitting in fixed buckets.
			end := start + 1
			for end < len(group) &&
				group[end].CorrectedTS-group[end-1].CorrectedTS <= chainWindow {
				end++
			}
			run := group[start:end]
			start = end

			ordered := make([]string, 0)
			seen := map[string]bool{}
			for _, e := range run {
				if !seen[e.Host] {
					seen[e.Host] = true
					ordered = append(ordered, e.Host)
				}
			}
			if len(ordered) < pivotMinHosts {
				continue
			}
			candidateCount++

			kept := ordered
			var dropped []string
			// #IR-5194: a run reaching further than max_chain_hosts hosts is cut at
			// that many, keeping the hosts first seen; the hosts beyond the cut are
			// queued rather than reported as part of the chain.
			wasCut := false
			if maxChainHosts > 0 && len(ordered) > maxChainHosts {
				kept = ordered[:maxChainHosts]
				dropped = ordered[maxChainHosts:]
				wasCut = true
			}
			keptSet := map[string]bool{}
			for _, h := range kept {
				keptSet[h] = true
			}

			var severity int64
			actionSet := map[string]bool{}
			first, last := int64(0), int64(0)
			count := 0
			for _, e := range run {
				if !keptSet[e.Host] {
					continue
				}
				// #IR-5188: a chain carries the severity of its single worst action,
				// not the sum of its actions.
				if s := actionSeverity[e.Action]; s > severity {
					severity = s
				}
				actionSet[e.Action] = true
				if count == 0 || e.CorrectedTS < first {
					first = e.CorrectedTS
				}
				if count == 0 || e.CorrectedTS > last {
					last = e.CorrectedTS
				}
				count++
			}
			actions := make([]string, 0, len(actionSet))
			for a := range actionSet {
				actions = append(actions, a)
			}
			sort.Strings(actions)

			chainID := account + ":" + run[0].EventID
			for _, h := range dropped {
				queue = append(queue, queueRow{chainID, account, h, severity, "chain_truncated"})
			}
			if severity < severityFloor {
				queue = append(queue, queueRow{chainID, account, kept[0], severity, "below_floor"})
				continue
			}
			// truncated_chain_count is a count of REPORTED chains that were cut, so
			// it is taken here rather than at the cut: a candidate cut at the host
			// cap and then dropped below the floor never reaches
			// incident_chains.json and is not one of them. Counting at the cut made
			// this the only summary field whose "reported" meant something different
			// from incident_chain_count's and max_severity's.
			if wasCut {
				truncatedCount++
			}
			chains = append(chains, chainRow{
				ChainID: chainID, Account: account, Hosts: kept, HostCount: len(kept),
				FirstTS: first, LastTS: last, EventCount: count,
				Severity: severity, Actions: actions,
			})
		}
	}

	// #IR-5196: chains are reported worst first, then earliest, then by chain id;
	// the queue is worst first, then by chain id, then by host.
	sort.Slice(chains, func(i, j int) bool {
		if chains[i].Severity != chains[j].Severity {
			return chains[i].Severity > chains[j].Severity
		}
		if chains[i].FirstTS != chains[j].FirstTS {
			return chains[i].FirstTS < chains[j].FirstTS
		}
		return chains[i].ChainID < chains[j].ChainID
	})
	sort.Slice(queue, func(i, j int) bool {
		if queue[i].Severity != queue[j].Severity {
			return queue[i].Severity > queue[j].Severity
		}
		if queue[i].ChainID != queue[j].ChainID {
			return queue[i].ChainID < queue[j].ChainID
		}
		return queue[i].Host < queue[j].Host
	})

	var maxSeverity int64
	for _, c := range chains {
		if c.Severity > maxSeverity {
			maxSeverity = c.Severity
		}
	}

	if err := os.MkdirAll(*outputDir, 0o755); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	summary := map[string]any{
		"schema_version":            "incident-triage-v1",
		"event_count":               len(events),
		"account_count":             len(byAccount),
		"host_count":                len(hosts),
		"session_count":             sessionCount,
		"chain_candidate_count":     candidateCount,
		"incident_chain_count":      len(chains),
		"truncated_chain_count":     truncatedCount,
		"queued_count":              len(queue),
		"max_severity":              maxSeverity,
		"effective_session_gap":     sessionGap,
		"effective_pivot_min_hosts": pivotMinHosts,
		"effective_severity_floor":  severityFloor,
		"effective_chain_window":    chainWindow,
		"effective_max_chain_hosts": maxChainHosts,
	}
	writeJSON(*outputDir+"/summary.json", summary)
	writeJSON(*outputDir+"/incident_chains.json", chains)

	handle, err := os.Create(*outputDir + "/triage_queue.jsonl")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	defer handle.Close()
	enc := json.NewEncoder(handle)
	for _, row := range queue {
		if err := enc.Encode(row); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}
	fmt.Fprintf(os.Stderr, "reported %d chains, queued %d\n", len(chains), len(queue))
}
