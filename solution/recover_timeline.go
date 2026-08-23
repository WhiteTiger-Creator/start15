// Stage one of the reference: rebuild the event timeline the collector truncated
// at /app/data/event_timeline.json.
//
// Governed by #IR-5170 (replay semantics), #IR-5174 (clock correction) and
// #IR-5178 (shape and ordering of the result).
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strconv"
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

type change struct {
	Seq     int    `json:"seq"`
	EventID string `json:"event_id"`
	Kind    string `json:"kind"`
	Field   string `json:"field"`
	Value   any    `json:"value"`
}

type sensorRow struct {
	Sensor        string `json:"sensor"`
	ClockOffsetSec int64 `json:"clock_offset_sec"`
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

func asInt64(v any) (int64, bool) {
	switch t := v.(type) {
	case float64:
		return int64(t), true
	case string:
		n, err := strconv.ParseInt(t, 10, 64)
		return n, err == nil
	}
	return 0, false
}

func setField(e *event, field string, value any) {
	switch field {
	case "account":
		if s, ok := value.(string); ok {
			e.Account = s
		}
	case "host":
		if s, ok := value.(string); ok {
			e.Host = s
		}
	case "action":
		if s, ok := value.(string); ok {
			e.Action = s
		}
	case "observed_ts":
		if n, ok := asInt64(value); ok {
			e.ObservedTS = n
		}
	}
}

func main() {
	var snapshot []event
	var journal []change
	var sensors []sensorRow
	readJSON("/app/data/event_snapshot_pre_truncation.json", &snapshot)
	readJSON("/app/data/collector_journal.json", &journal)
	readJSON("/app/data/sensor_registry.json", &sensors)

	offset := make(map[string]int64, len(sensors))
	for _, s := range sensors {
		offset[s.Sensor] = s.ClockOffsetSec
	}

	live := make(map[string]*event, len(snapshot))
	for i := range snapshot {
		e := snapshot[i]
		live[e.EventID] = &e
	}
	// #IR-5170: a retraction takes the event out but the collector keeps it, so a
	// later restore puts it back exactly as it stood when it was retracted --
	// amendments posted before the retraction survive, and any amendment posted
	// while it was out is lost.
	held := map[string]event{}

	sort.Slice(journal, func(i, j int) bool { return journal[i].Seq < journal[j].Seq })
	for _, c := range journal {
		switch c.Kind {
		case "amend":
			if e, ok := live[c.EventID]; ok {
				setField(e, c.Field, c.Value)
			}
		case "retract":
			if e, ok := live[c.EventID]; ok {
				held[c.EventID] = *e
				delete(live, c.EventID)
			}
		case "restore":
			if e, ok := held[c.EventID]; ok {
				restored := e
				live[c.EventID] = &restored
				delete(held, c.EventID)
			}
		}
	}

	out := make([]event, 0, len(live))
	for _, e := range live {
		// #IR-5174: the sensor's recorded offset is ADDED to the observed stamp to
		// reach the reference clock. A sensor the registry does not list keeps its
		// observed stamp unchanged.
		e.CorrectedTS = e.ObservedTS + offset[e.Sensor]
		out = append(out, *e)
	}
	// #IR-5178: ascending corrected timestamp, then event id on a tie.
	sort.Slice(out, func(i, j int) bool {
		if out[i].CorrectedTS != out[j].CorrectedTS {
			return out[i].CorrectedTS < out[j].CorrectedTS
		}
		return out[i].EventID < out[j].EventID
	})

	encoded, err := json.MarshalIndent(out, "", "  ")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := os.WriteFile("/app/data/event_timeline.json", append(encoded, '\n'), 0o644); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Fprintf(os.Stderr, "recovered %d events\n", len(out))
}
