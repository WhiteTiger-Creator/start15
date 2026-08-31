"""Verifier tests for this task.

Every test below corresponds to something instruction.md states is graded.
Shared machinery lives in harness.py.
"""

from harness import *  # noqa: F401,F403


@pytest.fixture(scope="session")
def primary_outputs():
    return _run_pipeline()


@pytest.fixture(scope="session")
def alternate_outputs():
    return _run_pipeline(input_path=ALT_INPUT)




# --------------------------------------------------------------------------
# Step one: the truncated timeline must be rebuilt before anything is grouped
# --------------------------------------------------------------------------
def test_recovery_sources_are_intact():
    """The snapshot, journal, registry, policy and shift log are read, not rewritten."""
    live = {n: hashlib.sha256(Path(p).read_bytes()).hexdigest() for n, p in (
        ("snapshot", SNAPSHOT_PATH), ("journal", JOURNAL_PATH),
        ("registry", DATA / "sensor_registry.json"),
        ("policy", DATA / "triage_policy.json"), ("log", LOG_PATH))}
    assert _digest(live) == FIXTURE["rule_sources_digest"]


def test_recovery_sources_are_still_intact_after_the_graded_run(primary_outputs):
    """Checked again once the engine has run, not only before it.

    The digest above is taken at collection, so byte-identity across the graded
    run rested on the candidate's file permissions rather than on a check.
    Depending on primary_outputs orders this one after the run, and the rebuilt
    timeline is included: the engine reads it and must not rewrite it.
    """
    live = {n: hashlib.sha256(Path(p).read_bytes()).hexdigest() for n, p in (
        ("snapshot", SNAPSHOT_PATH), ("journal", JOURNAL_PATH),
        ("registry", DATA / "sensor_registry.json"),
        ("policy", DATA / "triage_policy.json"), ("log", LOG_PATH))}
    assert _digest(live) == FIXTURE["rule_sources_digest"], (
        "an input was rewritten while the graded run was in flight")
    assert _digest(_load_json(TIMELINE_PATH)) == FIXTURE["recovered_timeline_digest"], (
        "the engine rewrote the timeline it was handed")


def test_timeline_was_recovered():
    """The rebuilt timeline matches the governed replay exactly."""
    recovered = _load_json(TIMELINE_PATH)
    assert len(recovered) == FIXTURE["recovered_event_count"]
    assert _digest(recovered) == FIXTURE["recovered_timeline_digest"]


def test_recovered_events_carry_only_the_declared_fields():
    """Collector bookkeeping never survives the replay."""
    for row in _load_json(TIMELINE_PATH):
        assert set(row) == EVENT_KEYS


def test_recovered_timeline_is_ordered_on_corrected_stamps():
    """The timeline ascends by corrected stamp, then event id."""
    rows = _load_json(TIMELINE_PATH)
    keys = [(r["corrected_ts"], r["event_id"]) for r in rows]
    assert keys == sorted(keys)


def test_corrected_stamp_adds_the_sensor_offset():
    """Every corrected stamp is the observed stamp plus its sensor's recorded offset."""
    offsets = {r["sensor"]: r["clock_offset_sec"] for r in _load_json(DATA / "sensor_registry.json")}
    for row in _load_json(TIMELINE_PATH):
        assert row["corrected_ts"] == row["observed_ts"] + offsets.get(row["sensor"], 0)


def test_an_event_on_an_unlisted_sensor_keeps_its_observed_stamp():
    """#IR-5174's fallback: a sensor the registry does not list corrects by nothing.

    Nothing in the shipped sources exercised this, so a rebuild that dropped such
    an event, or that failed on the missing offset, was never caught. EV-900001
    is carried on a sensor the registry has no row for.
    """
    offsets = {r["sensor"]: r["clock_offset_sec"] for r in _load_json(DATA / "sensor_registry.json")}
    rows = {r["event_id"]: r for r in _load_json(TIMELINE_PATH)}
    probe = rows.get("EV-900001")
    assert probe is not None, "the event on the unlisted sensor was dropped from the rebuild"
    assert probe["sensor"] not in offsets, "the probe's sensor is meant to be unlisted"
    assert probe["corrected_ts"] == probe["observed_ts"], (
        "an unlisted sensor was corrected by something rather than left alone")


def test_a_change_naming_an_event_the_snapshot_never_carried_is_ignored():
    """#IR-5170's fallback, and the bare restore beside it.

    The journal carries an amendment against EV-999999, which the snapshot never
    held, and a restore of EV-900001, which was never retracted. Neither may
    reach the rebuilt timeline: the first invents an event, the second would
    re-read one that never left.
    """
    rows = {r["event_id"]: r for r in _load_json(TIMELINE_PATH)}
    assert "EV-999999" not in rows, (
        "a change naming an event the snapshot never carried created one")
    journal = _load_json(JOURNAL_PATH)
    assert any(c["event_id"] == "EV-999999" for c in journal), "the probe change is missing"
    assert any(c["event_id"] == "EV-900001" and c["kind"] == "restore" for c in journal), \
        "the bare restore is missing"
    # the restore of an event that was never retracted left it exactly as it was
    snapshot = {r["event_id"]: r for r in _load_json(SNAPSHOT_PATH)}
    probe = rows["EV-900001"]
    assert probe["account"] == snapshot["EV-900001"]["account"]
    assert probe["observed_ts"] == snapshot["EV-900001"]["observed_ts"]


def test_wrong_replays_differ_from_the_governed_timeline():
    """Four plausible misreadings of the rebuild each give a different timeline.

    Concatenating the sources, replaying in file order, letting a restore re-read
    the snapshot, and subtracting the clock offset all diverge, so matching the
    sealed digest is evidence the governed rules were applied.
    """
    expected = FIXTURE["recovered_timeline_digest"]
    assert FIXTURE["shipped_truncated_digest"] != expected
    snapshot = {r["event_id"]: r for r in _load_json(SNAPSHOT_PATH)}
    journal = _load_json(JOURNAL_PATH)
    offsets = {r["sensor"]: r["clock_offset_sec"] for r in _load_json(DATA / "sensor_registry.json")}

    def replay(by_seq: bool, restore_from_snapshot: bool, sign: int):
        live = {k: dict(v) for k, v in snapshot.items()}
        held = {}
        for c in (sorted(journal, key=lambda x: x["seq"]) if by_seq else journal):
            eid, kind = c["event_id"], c["kind"]
            if kind == "amend" and eid in live:
                live[eid][c["field"]] = c["value"]
            elif kind == "retract" and eid in live:
                held[eid] = dict(live.pop(eid))
            elif kind == "restore":
                if restore_from_snapshot:
                    if eid in snapshot and eid not in live:
                        live[eid] = dict(snapshot[eid])
                elif eid in held:
                    live[eid] = held.pop(eid)
        rows = []
        for r in live.values():
            row = dict(r)
            row["corrected_ts"] = row["observed_ts"] + sign * offsets.get(row["sensor"], 0)
            rows.append(row)
        rows.sort(key=lambda r: (r["corrected_ts"], r["event_id"]))
        return _digest(rows)

    assert replay(False, False, 1) != expected     # file order
    assert replay(True, True, 1) != expected       # restore re-reads the snapshot
    assert replay(True, False, -1) != expected     # offset subtracted


# --------------------------------------------------------------------------
# Step two: the correlation itself
# --------------------------------------------------------------------------
def test_primary_summary_matches_fixture(primary_outputs):
    """Every summary field matches the sealed reference run."""
    _, summary, _, _ = primary_outputs
    assert summary == FIXTURE["primary"]["summary"]


def test_primary_artifacts_match_fixture(primary_outputs):
    """The chains and the triage queue match the sealed digests."""
    _, _, chains, queue = primary_outputs
    assert _digest(chains) == FIXTURE["primary"]["chains_digest"]
    assert _digest(queue) == FIXTURE["primary"]["queue_digest"]


def test_alternate_timeline_matches_fixture(alternate_outputs):
    """A held-out timeline the agent never sees produces the sealed result."""
    _, summary, chains, queue = alternate_outputs
    assert summary == FIXTURE["alternate"]["summary"]
    assert _digest(chains) == FIXTURE["alternate"]["chains_digest"]
    assert _digest(queue) == FIXTURE["alternate"]["queue_digest"]


def test_output_dir_contains_exactly_three_files(primary_outputs):
    """A run writes the three contracted artifacts and nothing else."""
    out_dir, _, _, _ = primary_outputs
    assert sorted(p.name for p in out_dir.iterdir()) == [
        "incident_chains.json", "summary.json", "triage_queue.jsonl"]


def test_summary_schema_and_types(primary_outputs):
    """The summary carries exactly the contracted fields at the contracted types."""
    _, summary, _, _ = primary_outputs
    assert set(summary) == SUMMARY_KEYS
    for field, kind in SPEC["outputs"]["summary"]["field_types"].items():
        value = summary[field]
        if kind == "integer":
            assert isinstance(value, int) and not isinstance(value, bool), field
        else:
            assert isinstance(value, str), field


def test_chain_schema_and_ordering(primary_outputs):
    """Chains carry the contracted fields and the contracted order."""
    _, _, chains, _ = primary_outputs
    keys = [(-c["severity"], c["first_ts"], c["chain_id"]) for c in chains]
    assert keys == sorted(keys)
    for c in chains:
        assert set(c) == CHAIN_KEYS
        assert c["host_count"] == len(c["hosts"])
        assert len(set(c["hosts"])) == len(c["hosts"])
        assert c["actions"] == sorted(c["actions"])
        assert c["first_ts"] <= c["last_ts"]
        assert c["chain_id"].startswith(c["account"] + ":")


def test_queue_schema_and_ordering(primary_outputs):
    """Queue rows carry the contracted fields and descend by severity."""
    _, _, _, queue = primary_outputs
    keys = [(-r["severity"], r["chain_id"], r["host"]) for r in queue]
    assert keys == sorted(keys)
    for r in queue:
        assert set(r) == QUEUE_KEYS
        assert r["reason"] in QUEUE_REASONS


def test_reported_chains_clear_the_floor_and_the_pivot(primary_outputs):
    """Every reported chain meets both admission rules."""
    _, summary, chains, _ = primary_outputs
    for c in chains:
        assert c["severity"] >= summary["effective_severity_floor"]
        assert c["host_count"] >= summary["effective_pivot_min_hosts"]
        assert c["host_count"] <= summary["effective_max_chain_hosts"]


def test_summary_counts_track_the_artifacts(primary_outputs):
    """The summary's own totals agree with the artifacts beside it."""
    _, summary, chains, queue = primary_outputs
    assert summary["incident_chain_count"] == len(chains)
    assert summary["queued_count"] == len(queue)
    assert summary["event_count"] == len(_load_json(TIMELINE_PATH))
    assert summary["max_severity"] == max((c["severity"] for c in chains), default=0)


def test_both_queue_reasons_occur(primary_outputs):
    """The graded timeline exercises every documented queue reason."""
    _, _, _, queue = primary_outputs
    assert {r["reason"] for r in queue} == QUEUE_REASONS


# --------------------------------------------------------------------------
# Each reversed rule, pinned on an instance where the drafts disagree
# --------------------------------------------------------------------------
BASE_POLICY = {"default": {"session_gap_sec": 1800, "pivot_min_hosts": 3,
                           "severity_floor": 40, "chain_window_sec": 7200,
                           "max_chain_hosts": 12}}


def _ev(eid, host, action, corrected, sensor="edr", account="svc-probe", offset=0):
    """A timeline row already carrying the corrected stamp the rebuild would give it."""
    return {"event_id": eid, "host": host, "account": account, "action": action,
            "sensor": sensor, "observed_ts": corrected - offset,
            "corrected_ts": corrected, "pid": 4242}


def _probe(events, policy=None):
    """Run the submitted engine over a crafted timeline and return its artifacts."""
    saved = (DATA / "triage_policy.json").read_text(encoding="utf-8")
    staged = _CWORK / f"probe-{next(_run_ctr)}.json"
    try:
        _write_json(DATA / "triage_policy.json", policy or BASE_POLICY)
        _write_json(staged, events)
        os.chmod(staged, 0o644)
        return _run_pipeline(input_path=staged)
    finally:
        (DATA / "triage_policy.json").write_text(saved, encoding="utf-8")


def test_chain_severity_is_the_worst_action_not_the_sum():
    """A three-host run of ordinary actions stays below the floor.

    Four logons and a process start sum to 25, which the summing interim would
    still hold under the floor, so the run also carries a share_mount at 20: the
    sum reaches 45 and would be reported, while the governed worst-action rule
    scores it 20 and queues it instead.
    """
    events = [
        _ev("EV-000001", "host-001", "logon", 100),
        _ev("EV-000002", "host-002", "logon", 200),
        _ev("EV-000003", "host-003", "share_mount", 300),
        _ev("EV-000004", "host-003", "logon", 400),
        _ev("EV-000005", "host-003", "process_start", 500),
    ]
    _, summary, chains, queue = _probe(events)
    assert summary["chain_candidate_count"] == 1
    assert chains == []
    assert [(r["severity"], r["reason"]) for r in queue] == [(20, "below_floor")]


def test_chain_window_is_measured_on_the_corrected_stamp():
    """The window closes on corrected stamps, not on the recorded ones.

    Every event sits inside the window once corrected, so the run holds three
    hosts and clears the pivot. Read on the observed stamps the third event lies
    far outside the window and the run would never reach three hosts.
    """
    events = [
        _ev("EV-000001", "host-001", "priv_escalate", 1000, sensor="edr", offset=0),
        _ev("EV-000002", "host-002", "logon", 2000, sensor="edr", offset=0),
        _ev("EV-000003", "host-003", "logon", 3000, sensor="auth", offset=-40000),
    ]
    _, summary, chains, _ = _probe(events)
    assert summary["chain_candidate_count"] == 1
    assert [c["host_count"] for c in chains] == [3]
    assert [c["severity"] for c in chains] == [45]


def test_run_past_the_host_cap_is_cut_and_the_excess_queued():
    """A run reaching past the cap keeps the hosts first seen and queues the rest."""
    events = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "priv_escalate", i * 100)
              for i in range(1, 16)]
    _, summary, chains, queue = _probe(events)
    assert summary["truncated_chain_count"] == 1
    assert [c["host_count"] for c in chains] == [12]
    assert chains[0]["hosts"] == [f"host-{i:03d}" for i in range(1, 13)]
    truncated = [r["host"] for r in queue if r["reason"] == "chain_truncated"]
    assert sorted(truncated) == [f"host-{i:03d}" for i in range(13, 16)]


def test_a_cut_chain_below_the_floor_is_not_a_truncated_chain():
    """truncated_chain_count counts REPORTED chains that were cut, not every cut.

    Thirteen hosts carry a logon, worth 5 each, so the run is cut at the cap and
    then falls below the floor of 40 and is queued rather than reported. It is a
    candidate and it was cut, but it never reaches incident_chains.json, so the
    contract's "reported chains that ran past the host cap and were cut" does not
    count it. Every other host-cap probe cuts a chain that IS reported, so none of
    them could tell the two readings apart.
    """
    events = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "logon", i * 100)
              for i in range(1, 14)]
    _, summary, chains, queue = _probe(events)
    assert summary["chain_candidate_count"] == 1, "the run cleared the pivot"
    assert chains == [], "a chain scoring 5 cannot clear the floor of 40"
    assert summary["truncated_chain_count"] == 0, (
        "a chain that was cut and then dropped below the floor was counted as a "
        "truncated chain, though it is never reported")
    assert {r["reason"] for r in queue} == {"chain_truncated", "below_floor"}


def test_an_action_the_table_does_not_name_contributes_nothing():
    """#IR-5186 fixes eight action severities and says an unnamed action is worth nothing.

    The crafted probes all used named actions, so nothing pinned this. Three hosts
    carry an action the table never names; the run clears the pivot and becomes a
    candidate, scores zero and is queued below the floor rather than reported.
    """
    events = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "quarantine_lifted", i * 100)
              for i in range(1, 4)]
    _, summary, chains, queue = _probe(events)
    assert summary["chain_candidate_count"] == 1
    assert chains == [], "an unnamed action gave the chain a severity"
    assert [r["reason"] for r in queue] == ["below_floor"]
    assert [r["severity"] for r in queue] == [0]


def test_a_policy_that_omits_a_field_keeps_the_governed_baseline():
    """#IR-5210 states the baselines a field the policy file omits falls back to.

    The probes always supplied every field, so the fallback was never exercised.
    Dropping pivot_min_hosts leaves the baseline of 3, which a two-host run does
    not reach and a three-host run does.
    """
    sparse = {"default": {"chain_window_sec": 7200, "session_gap_sec": 1800,
                          "severity_floor": 40, "max_chain_hosts": 12}}
    two = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "priv_escalate", i * 100)
           for i in range(1, 3)]
    _, summary, chains, _ = _probe(two, policy=sparse)
    assert summary["effective_pivot_min_hosts"] == 3, "the baseline was not restored"
    assert summary["chain_candidate_count"] == 0 and chains == []

    three = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "priv_escalate", i * 100)
             for i in range(1, 4)]
    _, summary, chains, _ = _probe(three, policy=sparse)
    assert summary["chain_candidate_count"] == 1
    assert [c["host_count"] for c in chains] == [3]


def test_a_session_breaks_on_the_gap_and_is_counted_per_host_and_account():
    """#IR-5182: a gap longer than session_gap_sec opens a new session.

    Nothing pinned session_count on its own; it rode on the two full-timeline
    comparisons, so a run counting sessions per account, or per host, or on the
    observed stamp, was caught only in bulk. Three events on one host for one
    account with a gap of 7200 across the second boundary make two sessions, and
    a second host under the same account makes a third.
    """
    gap = BASE_POLICY["default"]["session_gap_sec"]
    events = [
        _ev("EV-000001", "host-001", "logon", 100),
        _ev("EV-000002", "host-001", "logon", 100 + gap),          # inside the gap
        _ev("EV-000003", "host-001", "logon", 100 + gap + gap + 1),  # past it
        _ev("EV-000004", "host-002", "logon", 100),
    ]
    _, summary, _, _ = _probe(events)
    assert summary["session_count"] == 3, summary
    assert summary["host_count"] == 2 and summary["account_count"] == 1

    # the same events under two accounts split further, since a session belongs
    # to one host AND one account
    split = [
        _ev("EV-000001", "host-001", "logon", 100, account="svc-a"),
        _ev("EV-000002", "host-001", "logon", 200, account="svc-b"),
    ]
    _, summary, _, _ = _probe(split)
    assert summary["session_count"] == 2, summary


def test_a_run_below_the_pivot_is_not_a_candidate():
    """Two hosts do not make a chain, however severe the actions on them."""
    events = [
        _ev("EV-000001", "host-001", "log_cleared", 100),
        _ev("EV-000002", "host-002", "priv_escalate", 200),
    ]
    _, summary, chains, queue = _probe(events)
    assert summary["chain_candidate_count"] == 0
    assert chains == [] and queue == []


def test_events_beyond_the_cut_take_no_part_in_the_chain():
    """A worse action on a cut host does not raise the chain's severity.

    The twelve kept hosts carry a privilege escalation, scoring 45 and clearing the
    floor so the chain is reported. The thirteenth host, beyond the cut, carries a
    cleared log worth 50: were it counted the chain would score 50 instead.
    """
    events = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "priv_escalate", i * 100)
              for i in range(1, 13)]
    events.append(_ev("EV-000013", "host-013", "log_cleared", 1300))
    _, summary, chains, queue = _probe(events)
    assert summary["truncated_chain_count"] == 1
    assert [c["severity"] for c in chains] == [45]
    # #IR-5194: the actions the chain reports come from the kept hosts too, and
    # the queued row for the dropped host carries the cut-down chain severity
    # rather than the severity of the action that got it dropped.
    assert chains[0]["actions"] == ["priv_escalate"], chains[0]["actions"]
    truncated = [r for r in queue if r["reason"] == "chain_truncated"]
    assert [(r["host"], r["severity"]) for r in truncated] == [("host-013", 45)], truncated
    # the summary counts what was read, not what survived the cut
    assert summary["event_count"] == 13
    assert summary["host_count"] == 13


# --------------------------------------------------------------------------
# Contract, budget, determinism and isolation
# --------------------------------------------------------------------------
def test_a_run_writes_nothing_outside_its_output_directory():
    """instruction.md scopes an engine run to its --output-dir, and nothing checked it.

    Every other run here reads the three artifacts by name, so a run that also
    dropped a scratch file beside them, or in the directory it was started from,
    satisfied all of them. This walks the whole work area afterwards.
    """
    _publish_inputs()
    work = _candidate_dir()
    out_dir = work / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(out_dir, 0o777)
    staged = work / "timeline.json"
    shutil.copyfile(str(TIMELINE_PATH), str(staged))
    os.chmod(staged, 0o644)

    before = {str(q.relative_to(work)) for q in work.rglob("*")}
    binary = _build(WORKFLOW_PATH)
    result = _run_agent([binary, "--input", str(staged), "--output-dir", str(out_dir)], cwd=work)
    assert result.returncode == 0, result.stderr
    after = {str(q.relative_to(work)) for q in work.rglob("*")}
    written = sorted(after - before)
    assert written == ["output/incident_chains.json", "output/summary.json",
                       "output/triage_queue.jsonl"], written


def test_a_changed_policy_value_changes_the_run_it_governs():
    """Each policy field has to reach the calculation, not just the summary.

    Every crafted world in this suite stages the shipped defaults, and the
    influence test below only asks that the effective_* fields move and that the
    summary differs -- which those fields alone satisfy. An engine could read the
    policy to fill them and use five hardcoded values everywhere else and pass.
    Each case here changes ONE value and requires the sessions, candidates,
    chains or queue it governs to move with it.
    """
    def policy(**changed):
        merged = dict(BASE_POLICY["default"])
        merged.update(changed)
        return {"default": merged}

    # session_gap_sec: two events 1000s apart on one host and account
    pair = [_ev("EV-000001", "host-001", "logon", 100),
            _ev("EV-000002", "host-001", "logon", 1100)]
    _, wide, _, _ = _probe(pair, policy=policy(session_gap_sec=1800))
    _, narrow, _, _ = _probe(pair, policy=policy(session_gap_sec=500))
    assert wide["session_count"] == 1, wide
    assert narrow["session_count"] == 2, (
        "session_gap_sec did not reach the session count")

    # pivot_min_hosts: a three-host run is a candidate at 3 and not at 4
    three = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "priv_escalate", i * 100)
             for i in range(1, 4)]
    _, at_three, _, _ = _probe(three, policy=policy(pivot_min_hosts=3))
    _, at_four, _, _ = _probe(three, policy=policy(pivot_min_hosts=4))
    assert at_three["chain_candidate_count"] == 1
    assert at_four["chain_candidate_count"] == 0, (
        "pivot_min_hosts did not reach chain formation")

    # severity_floor: a chain scoring 45 clears 40 and not 50
    _, under, chains_under, _ = _probe(three, policy=policy(severity_floor=40))
    _, over, chains_over, queue_over = _probe(three, policy=policy(severity_floor=50))
    assert under["incident_chain_count"] == 1 and chains_under
    assert over["incident_chain_count"] == 0 and chains_over == [], (
        "severity_floor did not reach the reported set")
    assert {row["reason"] for row in queue_over} == {"below_floor"}

    # chain_window_sec: hosts 5000s apart form one run at 7200 and not at 1000
    spread = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "priv_escalate", i * 5000)
              for i in range(1, 4)]
    _, wide_window, _, _ = _probe(spread, policy=policy(chain_window_sec=7200))
    _, tight_window, _, _ = _probe(spread, policy=policy(chain_window_sec=1000))
    assert wide_window["chain_candidate_count"] == 1
    assert tight_window["chain_candidate_count"] == 0, (
        "chain_window_sec did not reach the run boundaries")

    # max_chain_hosts: a five-host run is whole at 12 and cut at 3
    five = [_ev(f"EV-{i:06d}", f"host-{i:03d}", "priv_escalate", i * 100)
            for i in range(1, 6)]
    _, uncut, chains_uncut, queue_uncut = _probe(five, policy=policy(max_chain_hosts=12))
    _, cut, chains_cut, queue_cut = _probe(five, policy=policy(max_chain_hosts=3))
    assert [c["host_count"] for c in chains_uncut] == [5]
    assert uncut["truncated_chain_count"] == 0
    assert [c["host_count"] for c in chains_cut] == [3], (
        "max_chain_hosts did not reach the host cap")
    assert cut["truncated_chain_count"] == 1
    assert len([r for r in queue_cut if r["reason"] == "chain_truncated"]) == 2
    assert not [r for r in queue_uncut if r["reason"] == "chain_truncated"]


def test_policy_path_actually_influences_the_output():
    """The policy is resolved from its fixed path, not inlined as constants."""
    saved = (DATA / "triage_policy.json").read_text(encoding="utf-8")
    try:
        _write_json(DATA / "triage_policy.json", {"default": {
            "session_gap_sec": 900, "pivot_min_hosts": 5, "severity_floor": 12,
            "chain_window_sec": 3600, "max_chain_hosts": 6}})
        _, summary, _, _ = _run_pipeline()
        assert summary["effective_session_gap"] == 900
        assert summary["effective_pivot_min_hosts"] == 5
        assert summary["effective_severity_floor"] == 12
        assert summary["effective_chain_window"] == 3600
        assert summary["effective_max_chain_hosts"] == 6
        assert summary != FIXTURE["primary"]["summary"]
    finally:
        (DATA / "triage_policy.json").write_text(saved, encoding="utf-8")


def test_run_is_idempotent(primary_outputs):
    """Re-running over the same timeline reproduces the same artifacts."""
    _, summary, chains, queue = primary_outputs
    _, s2, c2, q2 = _run_pipeline()
    assert s2 == summary and _digest(c2) == _digest(chains) and _digest(q2) == _digest(queue)


def test_artifacts_are_serialised_exactly_as_the_contract_states(primary_outputs):
    """Serialisation is contracted, and the digests cannot see it.

    _digest decodes before hashing, so an artifact with the right content and the
    wrong layout matches every sealed fixture. The contract names two-space indent
    with a trailing newline for the JSON artifacts and one compact object per line
    for the queue, so those are read off the raw bytes here.
    """
    out_dir = primary_outputs[0]
    for name in ("incident_chains.json", "summary.json"):
        raw = (out_dir / name).read_text(encoding="utf-8")
        assert raw.endswith("\n"), f"{name} has no trailing newline"
        assert not raw.endswith("\n\n"), f"{name} ends with a blank line"
        assert raw == json.dumps(json.loads(raw), indent=2) + "\n", (
            f"{name} is not two-space-indented JSON with a trailing newline")

    raw = (out_dir / "triage_queue.jsonl").read_text(encoding="utf-8")
    assert raw.endswith("\n"), "triage_queue.jsonl has no trailing newline"
    lines = raw.splitlines()
    assert lines and all(line.strip() for line in lines), "the queue carries a blank line"
    for number, line in enumerate(lines, start=1):
        assert ": " not in line, f"queue line {number} is not compact"
        assert json.dumps(json.loads(line), separators=(",", ":")) == line, (
            f"queue line {number} is not the compact serialisation of its own content")


def test_recovered_timeline_is_serialised_exactly_as_the_contract_states():
    """The rebuilt timeline carries the layout the contract names, not just the content."""
    raw = TIMELINE_PATH.read_text(encoding="utf-8")
    assert raw.endswith("\n"), "the timeline has no trailing newline"
    assert raw == json.dumps(json.loads(raw), indent=2) + "\n", (
        "the rebuilt timeline is not two-space-indented JSON with a trailing newline")


def test_no_argument_run_writes_to_the_documented_defaults(primary_outputs):
    """With no flags at all the program reads and writes its documented defaults.

    The previous form still passed --output-dir, so it only exercised the --input
    default; a changed default output directory went unnoticed.
    """
    binary = _build(WORKFLOW_PATH)
    _publish_inputs()
    default_out = Path("/app/output")
    shutil.rmtree(default_out, ignore_errors=True)
    default_out.mkdir(parents=True, exist_ok=True)
    os.chmod(default_out, 0o777)
    result = _run_agent([binary], cwd=_candidate_dir())
    assert result.returncode == 0, result.stderr
    assert sorted(q.name for q in default_out.iterdir()) == ['incident_chains.json', 'summary.json', 'triage_queue.jsonl']
    _, summary, doc, queue = primary_outputs
    assert _load_json(default_out / "summary.json") == summary
    assert _digest(_load_json(default_out / "incident_chains.json")) == _digest(doc)
    assert _digest(_load_jsonl(default_out / "triage_queue.jsonl")) == _digest(queue)


def test_the_budget_is_enforced_by_killing_an_overrunning_run(primary_outputs):
    """The budget is enforced, and not by timing the grading machine.

    Every candidate run is executed with the contract's published budget as its
    hard timeout, so a run that overruns is killed and the suite fails. Nothing
    compares a measured elapsed time against a threshold.
    """
    assert HARD_TIMEOUT_SEC == int(RUNTIME_BUDGET_SEC)
    assert primary_outputs[1]["incident_chain_count"] > 0, "the graded run did not complete"



def test_runtime_budget_is_stated_in_the_contract():
    """The budget enforced above is the one the contract publishes."""
    assert int(SPEC["runtime_budget_seconds"]) == int(RUNTIME_BUDGET_SEC)


def test_submitted_program_runs_unprivileged_and_cannot_write_reward(tmp_path):
    """The graded program runs as nobody and cannot touch the reward path."""
    probe = tmp_path / "main.go"
    probe.write_text(
        'package main\n\nimport ("fmt"; "os")\n\n'
        'func main() {\n\tfmt.Println(os.Getuid())\n'
        '\terr := os.WriteFile("/logs/verifier/reward.txt", []byte("1"), 0o644)\n'
        '\tfmt.Println(err != nil)\n}\n', encoding="utf-8")
    binary = _build(probe)
    result = _run_agent([binary], cwd=_candidate_dir())
    assert result.returncode == 0, result.stderr
    parts = result.stdout.split()
    assert parts[0] == str(CANDIDATE_UID) and parts[1] == "true"


def test_frozen_snapshot_preserved():
    """The collector's engine must still be on disk, unmodified."""
    assert ORIGINAL_WORKFLOW_PATH.exists()
    assert hashlib.sha256(ORIGINAL_WORKFLOW_PATH.read_bytes()).hexdigest() == \
        FIXTURE["broken_engine_sha256"]


def test_frozen_snapshot_is_wrong(primary_outputs):
    """The shipped engine does not already produce the governed report."""
    _, summary, _, _ = primary_outputs
    _, broken, _, _ = _run_pipeline(script_path=ORIGINAL_WORKFLOW_PATH)
    assert broken != summary


def test_governance_log_present():
    """The shift log the rules are reconstructed from is in the environment."""
    assert LOG_PATH.exists() and LOG_PATH.stat().st_size > 0


def test_shipped_contract_matches_the_golden_copy():
    """The output contract in the environment is unmodified.

    Field lists, container shapes and sort orders are golden metadata and are read
    from the verifier's own image; this proves the agent's copy still agrees with
    it, so the contract cannot be trimmed to weaken a schema check.
    """
    shipped = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    assert shipped == json.loads(GOLDEN_CONTRACT_PATH.read_text(encoding="utf-8"))

