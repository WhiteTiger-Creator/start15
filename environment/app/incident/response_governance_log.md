# Planning governance log

How the incident-correlation engine is *meant* to behave -- the recovery of the truncated event timeline, the clock correction, the basis for every boundary, action severity, chain formation and the handling of an oversized chain -- was settled incrementally by the incident-response board, and those decisions live in the review entries below, not in any single summary. Where two entries speak to the same stage, the later dated decision governs. `/app/docs/triage_contract.json` is the output contract only.

- 2026-02-07: The escalation desk noted a routine observation. The nightly integrity check over the journal completed clean. The thread was archived after review.

> **Recovery draft proposal (2026-02-07 - #IR-5020)** Rosa: rebuild the truncated timeline by concatenating the pre-truncation snapshot with the collector journal and keeping the last row seen for each event id; a restored event is re-read from the snapshot.

> **Recovery draft proposal (2026-02-14 - #IR-5026)** Anders: a sensor's recorded clock offset is SUBTRACTED from the observed stamp to reach the reference clock.

> **Recovery draft proposal (2026-02-20 - #IR-5032)** Marek: session and window boundaries are drawn on the stamp the sensor recorded, since that is the figure the analyst sees in the console.

- 2026-02-09: The SOC lead spot-checked a routine observation. A collector fell behind for a few minutes and caught up without gaps in the feed.

- 2026-02-09: The triage queue owner spot-checked a routine observation. The registry of sensors was reconciled against the inventory with no drift found. Nothing here bears on engine behaviour.

- 2026-02-07: A responder on shift reviewed a routine observation. A tabletop exercise was scheduled; no production system was touched.

- 2026-02-20: The collector owner raised and closed a routine observation. One sensor reported a clock step after an NTP resync; the offset table was unchanged. No action was carried forward.

- 2026-02-13: A shift handover spot-checked a routine observation. An analyst asked whether a session had already been closed; it had, in the prior window. The thread was archived after review.

- 2026-02-15: An on-call engineer signed off a routine observation. The case queue sat slightly above its running mean, entirely from low-severity items.

- 2026-02-21: An on-call engineer signed off a routine observation. Storage headroom on the collector was reported comfortable for the quarter.

- 2026-02-20: The detection-engineering desk signed off a routine observation. A noisy detection rule was tuned at source and stopped firing on maintenance traffic. Filed for the record.

- 2026-02-06: A weekly detection review noted a routine observation. Two alerts deduplicated to one case after the correlation pass ran.

- 2026-02-09: The sensor platform team carried forward a routine observation. One sensor reported a clock step after an NTP resync; the offset table was unchanged. No action was carried forward.

- 2026-02-22: The triage queue owner recorded a routine observation. One sensor reported a clock step after an NTP resync; the offset table was unchanged. Recorded without further action.

- 2026-02-23: The collector owner reviewed a routine observation. An enrichment lookup timed out once and succeeded on retry.

- 2026-02-09: The triage queue owner reviewed a routine observation. The case queue sat slightly above its running mean, entirely from low-severity items. No action was carried forward.

- 2026-02-04: The escalation desk recorded a routine observation. The on-call handover recorded nothing outstanding for the next shift. Logged for trend purposes only.

- 2026-02-19: A weekly detection review raised and closed a routine observation. A responder asked for the previous window's export and was pointed at the archive. The thread was archived after review.

- 2026-02-15: The sensor platform team minuted a routine observation. The registry of sensors was reconciled against the inventory with no drift found. The thread was archived after review.

- 2026-02-09: The duty analyst filed a routine observation. The registry of sensors was reconciled against the inventory with no drift found. Nothing here bears on engine behaviour.

- 2026-02-13: A responder on shift recorded a routine observation. The on-call handover recorded nothing outstanding for the next shift. Referred to the dated decisions and closed.

- 2026-02-12: The triage queue owner reviewed a routine observation. The nightly integrity check over the journal completed clean.

- 2026-02-02: The triage queue owner reviewed a routine observation. The on-call handover recorded nothing outstanding for the next shift.

- 2026-02-10: A responder on shift signed off a routine observation. The nightly integrity check over the journal completed clean. Nothing here bears on engine behaviour.

- 2026-03-19: A weekly detection review opened a query on a routine observation. One sensor reported a clock step after an NTP resync; the offset table was unchanged.

> **Interim decision (2026-03-06 - #IR-5044)** Priya: a chain carries the SUM of the severities of the actions observed along it.

> **Interim decision (2026-03-11 - #IR-5050)** Priya: every candidate clearing the severity floor is reported on its own account, however close it sits to the one before it. The desk would rather see a repeat twice than miss it once.

- 2026-03-06: The SOC lead logged a routine observation. The registry of sensors was reconciled against the inventory with no drift found. Noted and closed.

- 2026-03-27: The triage queue owner recorded a routine observation. An enrichment lookup timed out once and succeeded on retry. The thread was archived after review.

- 2026-03-03: An on-call engineer signed off a routine observation. A vendor advisory was reviewed and found not to affect this deployment. Filed for the record.

- 2026-03-08: The sensor platform team signed off a routine observation. An analyst asked whether a session had already been closed; it had, in the prior window. Filed for the record.

- 2026-03-23: The triage queue owner carried forward a routine observation. A responder asked for the previous window's export and was pointed at the archive. No dissent was recorded.

- 2026-03-14: The SOC lead filed a routine observation. One sensor's feed was replayed after a broker restart, producing no duplicates downstream. Logged for trend purposes only.

- 2026-03-21: The duty analyst spot-checked a routine observation. Storage headroom on the collector was reported comfortable for the quarter. No dissent was recorded.

- 2026-03-17: A weekly detection review logged a routine observation. A collector fell behind for a few minutes and caught up without gaps in the feed. Filed for the record.

- 2026-03-17: An on-call engineer recorded a routine observation. An enrichment lookup timed out once and succeeded on retry. Referred to the dated decisions and closed.

- 2026-03-25: The detection-engineering desk logged a routine observation. One event arrived with a malformed field and was quarantined by the parser. The desk confirmed no case impact.

- 2026-03-13: The collector owner carried forward a routine observation. A collector fell behind for a few minutes and caught up without gaps in the feed. Closed with no parameter change.

- 2026-03-16: The sensor platform team spot-checked a routine observation. The evidence store was rotated on schedule with no loss of retained events. A second reviewer concurred.

- 2026-03-10: The sensor platform team opened a query on a routine observation. An account lockout was traced to a stale credential in a scheduled job, not an intrusion. Logged for trend purposes only.

- 2026-03-25: A weekly detection review spot-checked a routine observation. A vendor advisory was reviewed and found not to affect this deployment.

- 2026-03-15: The forensics reviewer reviewed a routine observation. One sensor's feed was replayed after a broker restart, producing no duplicates downstream. A second reviewer concurred.

- 2026-03-01: The duty analyst carried forward a routine observation. An account lockout was traced to a stale credential in a scheduled job, not an intrusion.

- 2026-03-22: The detection-engineering desk reviewed a routine observation. A noisy detection rule was tuned at source and stopped firing on maintenance traffic. No follow-up was requested.

- 2026-03-24: A shift handover opened a query on a routine observation. The nightly integrity check over the journal completed clean. Nothing here bears on engine behaviour.

- 2026-03-07: The collector owner signed off a routine observation. Two alerts deduplicated to one case after the correlation pass ran.

- 2026-03-07: The forensics reviewer reviewed a routine observation. An account lockout was traced to a stale credential in a scheduled job, not an intrusion. Noted and closed.

- 2026-04-08: The forensics reviewer spot-checked a routine observation. The on-call handover recorded nothing outstanding for the next shift.

- 2026-04-18: A shift handover reviewed a routine observation. One sensor's feed was replayed after a broker restart, producing no duplicates downstream. Filed for the record.

- 2026-04-17: The collector owner logged a routine observation. A tabletop exercise was scheduled; no production system was touched. Filed for the record.

- 2026-04-03: The detection-engineering desk reviewed a routine observation. One event arrived with a malformed field and was quarantined by the parser. Logged for trend purposes only.

- 2026-04-22: The duty analyst raised and closed a routine observation. The case queue sat slightly above its running mean, entirely from low-severity items.

- 2026-04-13: The forensics reviewer spot-checked a routine observation. An enrichment lookup timed out once and succeeded on retry. Nothing here bears on engine behaviour.

- 2026-04-01: A weekly detection review minuted a routine observation. The case queue sat slightly above its running mean, entirely from low-severity items. No action was carried forward.

- 2026-04-22: The detection-engineering desk logged a routine observation. The on-call handover recorded nothing outstanding for the next shift.

- 2026-04-06: A responder on shift logged a routine observation. The evidence store was rotated on schedule with no loss of retained events. Logged for trend purposes only.

- 2026-04-03: The triage queue owner logged a routine observation. A host dropped off the inventory during a rebuild and returned the same evening.

- 2026-04-17: A responder on shift opened a query on a routine observation. A vendor advisory was reviewed and found not to affect this deployment. Filed for the record.

- 2026-04-27: The sensor platform team raised and closed a routine observation. One event arrived with a malformed field and was quarantined by the parser.

- 2026-04-24: A responder on shift raised and closed a routine observation. The on-call handover recorded nothing outstanding for the next shift.

- 2026-04-14: The triage queue owner noted a routine observation. A firewall change window overlapped the collection window and was noted for context. Filed for the record.

- 2026-04-17: The detection-engineering desk minuted a routine observation. The nightly integrity check over the journal completed clean.

- 2026-04-04: The duty analyst carried forward a routine observation. The evidence store was rotated on schedule with no loss of retained events.

- 2026-04-23: A responder on shift spot-checked a routine observation. The nightly integrity check over the journal completed clean.

- 2026-04-13: An on-call engineer carried forward a routine observation. A noisy detection rule was tuned at source and stopped firing on maintenance traffic. The thread was archived after review.

- 2026-04-15: The collector owner logged a routine observation. Two alerts deduplicated to one case after the correlation pass ran. Noted and closed.

- 2026-04-11: The forensics reviewer recorded a routine observation. A host dropped off the inventory during a rebuild and returned the same evening. No dissent was recorded.

- 2026-05-02: The SOC lead raised and closed a routine observation. An enrichment lookup timed out once and succeeded on retry. Recorded without further action.

> **Governance decision (2026-05-05 - #IR-5150)** Priya: Input paths, final. The triage policy is always read from its fixed absolute path under /app/data; `--input` selects the event timeline only. Both `--input` and `--output-dir` keep their documented defaults.

> **Governance decision (2026-05-08 - #IR-5170)** Yusuf: Timeline recovery, final. Start from the pre-truncation snapshot and replay the collector journal in ascending `seq`, never in file order. Each journal record carries `seq`, the `event_id` it acts on, a `kind` of `amend`, `retract` or `restore`, and for an amendment the `field` it names and the `value` it sets; `posted_by` is the collector's own bookkeeping and settles nothing. An `amend` overwrites the named field in place. A `retract` takes the event out of the timeline, but the collector keeps it as it stood at that moment. A `restore` puts a retracted event back EXACTLY as it stood when it was retracted: amendments posted before the retraction survive, and any amendment posted while it was out is lost. A change naming an event the snapshot never carried is ignored, and a restore of an event that was never retracted does nothing. Two more that came up in review: a retraction of an event already out does nothing either -- the state held aside stays the one captured at the first retraction, not a later one -- and an amendment naming a field the record does not declare is ignored, as is one naming `event_id`, which is the identity the replay is keyed on, or `corrected_ts`, which is derived from the observed stamp rather than stored.

> **Governance decision (2026-05-11 - #IR-5174)** Yusuf: Clock correction, final. Each event carries a corrected stamp reached by ADDING its sensor's recorded `clock_offset_sec` to the observed stamp. An event whose sensor the registry does not list keeps its observed stamp as its corrected stamp.

> **Governance decision (2026-05-13 - #IR-5178)** Lena: Recovered shape, final. The rebuilt timeline is a JSON array ascending by corrected stamp and, on a tie, by `event_id`. Each record carries the eight declared fields -- the collector's bookkeeping (`seq`, `kind`, `posted_by`) never survives the replay.

> **Governance decision (2026-05-16 - #IR-5182)** Lena: Boundary basis, final. Every boundary in this procedure -- the session gap and the chain window alike -- is measured on the CORRECTED stamp and never on the stamp the sensor recorded. A session opens on a host for an account whenever the gap from that account's previous event on that host exceeds the policy's `session_gap_sec`. The account's FIRST event on a host opens a session there as well, having no previous event to be measured against, so a host an account touched at all counts at least one session and `session_count` is the number of sessions across every host and account rather than the number of gaps that opened one.

> **Governance decision (2026-05-19 - #IR-5186)** Marek: Action severity, final. The board fixes the severity of an observed action at: logon 5; logon_failed 8; process_start 10; net_connect 12; file_write 15; share_mount 20; priv_escalate 45; log_cleared 50. An action this table does not name contributes nothing.

> **Governance decision (2026-05-24 - #IR-5192)** Marek: Chain identity, final. A chain's `chain_id` is its account, a single colon, and the `event_id` of the earliest event on the chain in the #IR-5182 corrected-stamp order, written `account:event_id` with no spaces. The identifier is formed BEFORE the #IR-5194 host cap truncates anything, so a chain that loses hosts to the cap keeps the identifier it already had, and every `chain_truncated` row the cap queues carries that same identifier alongside the host it dropped.

> **Governance decision (2026-05-22 - #IR-5188)** Marek: Chain severity, final. A chain carries the severity of its single worst action, not the sum of the actions observed along it. A chain whose severity falls below the policy's `severity_floor` is not reported as an incident and is queued as `below_floor` instead. That queue row names the chain's FIRST host in first-seen order, the same host the chain would have reported first, and one row is queued per chain rather than one per host.

> **Governance decision (2026-05-25 - #IR-5190)** Priya: Chain formation, final. An account's events are taken in corrected order and a run closes as soon as the next event lies further than the policy's `chain_window_sec` from the one before it, so the window slides with the activity rather than sitting in fixed buckets. A run is a chain candidate only where it touches at least `pivot_min_hosts` distinct hosts.

> **Governance decision (2026-05-28 - #IR-5194)** Yusuf: Oversized chains, final. A candidate reaching further than `max_chain_hosts` distinct hosts is cut at that many, keeping the hosts in the order they were first seen; every host beyond the cut is queued as `chain_truncated` and the events on those hosts take no part in the chain's severity, its span, its event count or the list of actions it reports: the chain is read as though the hosts beyond the cut were never on it. The severity a `chain_truncated` row carries is that same cut-down chain severity, one row per dropped host, so every row the cap queues for one chain carries the same severity as the chain itself. None of this reaches the run summary, whose `event_count` and `host_count` count the events read and the distinct hosts among them across the whole file, whether or not a cap later dropped a host from a chain. `truncated_chain_count` does count the cut, but only over chains the run REPORTS: a candidate cut at the cap and then dropped below the #IR-5188 severity floor is queued rather than reported, and is not one of them. The board notes the two readings differ widely on a real timeline, so the distinction is not academic.

> **Governance decision (2026-05-30 - #IR-5196)** Lena: Emission order, final. A chain is identified by its account and the event id it opens on. Chains are reported worst severity first, then earliest first stamp, then by chain id. The triage queue is worst severity first, then by chain id, then by host.

> **Governance decision (2026-05-30 - #IR-5198)** Lena: Run summary, final. The counters are aggregates of what the run itself read and emitted. `event_count`, `account_count` and `host_count` are the events in the timeline handed to `--input` and the distinct accounts and hosts they name. `session_count` is the sessions those events fall into once the #IR-5182 gap is applied. `chain_candidate_count` is the runs that became candidates under #IR-5190, so the severity floor has not been applied to it yet, while `incident_chain_count` is what `incident_chains.json` reports and `queued_count` the rows in `triage_queue.jsonl` with both reasons together. `max_severity` is the greatest severity among the REPORTED chains, so a candidate that fell below the floor does not raise it, and it is 0 when nothing is reported. The `effective_*` fields are the policy values in force, whether they came from the policy file or from the #IR-5210 baseline.

- 2026-05-09: The SOC lead recorded a routine observation. The evidence store was rotated on schedule with no loss of retained events.

- 2026-05-18: The detection-engineering desk minuted a routine observation. The case queue sat slightly above its running mean, entirely from low-severity items. The desk confirmed no case impact.

- 2026-05-07: The duty analyst spot-checked a routine observation. The nightly integrity check over the journal completed clean.

- 2026-05-02: The duty analyst recorded a routine observation. A responder asked for the previous window's export and was pointed at the archive. Nothing here bears on engine behaviour.

- 2026-05-17: The SOC lead minuted a routine observation. A collector fell behind for a few minutes and caught up without gaps in the feed.

- 2026-05-02: The duty analyst spot-checked a routine observation. A vendor advisory was reviewed and found not to affect this deployment. Logged for trend purposes only.

- 2026-05-27: The SOC lead filed a routine observation. The nightly integrity check over the journal completed clean.

- 2026-05-25: An on-call engineer raised and closed a routine observation. A collector fell behind for a few minutes and caught up without gaps in the feed.

- 2026-05-19: The sensor platform team spot-checked a routine observation. An account lockout was traced to a stale credential in a scheduled job, not an intrusion.

- 2026-05-14: The duty analyst noted a routine observation. A host dropped off the inventory during a rebuild and returned the same evening. No follow-up was requested.

- 2026-05-06: A responder on shift noted a routine observation. One sensor's feed was replayed after a broker restart, producing no duplicates downstream.

- 2026-05-20: A shift handover logged a routine observation. The registry of sensors was reconciled against the inventory with no drift found.

- 2026-05-07: A shift handover minuted a routine observation. Two alerts deduplicated to one case after the correlation pass ran. Closed with no parameter change.

- 2026-05-11: The triage queue owner reviewed a routine observation. A responder asked for the previous window's export and was pointed at the archive.

- 2026-05-09: A responder on shift signed off a routine observation. One sensor reported a clock step after an NTP resync; the offset table was unchanged. Closed with no parameter change.

- 2026-05-06: A responder on shift opened a query on a routine observation. The evidence store was rotated on schedule with no loss of retained events.

- 2026-05-11: The sensor platform team noted a routine observation. Two alerts deduplicated to one case after the correlation pass ran. Recorded without further action.

- 2026-05-11: The detection-engineering desk raised and closed a routine observation. An account lockout was traced to a stale credential in a scheduled job, not an intrusion. No dissent was recorded.

- 2026-05-19: A responder on shift recorded a routine observation. A noisy detection rule was tuned at source and stopped firing on maintenance traffic. Noted and closed.

- 2026-06-21: The triage queue owner noted a routine observation. An account lockout was traced to a stale credential in a scheduled job, not an intrusion. The thread was archived after review.

> **Governance decision (2026-06-04 - #IR-5210)** Priya: Triage policy baseline, read from /app/data/triage_policy.json at that fixed absolute path. Any field the policy file omits keeps its baseline: session_gap_sec = 1800; pivot_min_hosts = 3; severity_floor = 40; chain_window_sec = 7200; max_chain_hosts = 12.

> **Governance decision (2026-06-04 - #IR-5214)** Priya: Repeat suppression, final. A candidate that clears the floor is reported only where it stands clear of the account's previous report: where its first corrected stamp falls within the policy's `repeat_suppress_sec` of the LAST corrected stamp of the chain most recently reported for that account, it is queued as `superseded` instead, one row naming its first host in first-seen order and carrying its own severity. The desk is already reading the earlier chain and the repeat adds nothing to the page. Three things the review pinned. The floor is applied first, so a candidate queued as `below_floor` was never reported and starts no suppression of its own. Suppression does not chain either: a candidate queued as `superseded` is not itself a report, so the next candidate is measured against the last chain actually REPORTED and not against the one just suppressed. And a suppressed chain is not a reported chain anywhere else in the summary -- it raises no `max_severity`, and a candidate cut at the host cap and then suppressed is not one of the `truncated_chain_count`, on the same reading #IR-5194 already gives the floor.

> **Governance decision (2026-06-06 - #IR-5216)** Priya: Triage policy baseline, addendum. `repeat_suppress_sec` keeps a baseline of 900 where the policy file omits it.

- 2026-06-21: The sensor platform team carried forward a routine observation. An enrichment lookup timed out once and succeeded on retry.

- 2026-06-03: The SOC lead filed a routine observation. The evidence store was rotated on schedule with no loss of retained events. No dissent was recorded.

- 2026-06-02: The collector owner logged a routine observation. The case queue sat slightly above its running mean, entirely from low-severity items. Referred to the dated decisions and closed.

- 2026-06-18: The sensor platform team signed off a routine observation. The registry of sensors was reconciled against the inventory with no drift found.

- 2026-06-17: The triage queue owner opened a query on a routine observation. Two alerts deduplicated to one case after the correlation pass ran. Filed for the record.

- 2026-06-02: An on-call engineer recorded a routine observation. One sensor's feed was replayed after a broker restart, producing no duplicates downstream. Referred to the dated decisions and closed.

- 2026-06-24: A shift handover minuted a routine observation. An enrichment lookup timed out once and succeeded on retry.

- 2026-06-02: A weekly detection review reviewed a routine observation. The on-call handover recorded nothing outstanding for the next shift. Logged for trend purposes only.

- 2026-06-12: The collector owner recorded a routine observation. Two alerts deduplicated to one case after the correlation pass ran. A second reviewer concurred.

- 2026-06-18: The forensics reviewer signed off a routine observation. A firewall change window overlapped the collection window and was noted for context. No action was carried forward.

- 2026-06-23: A weekly detection review noted a routine observation. A collector fell behind for a few minutes and caught up without gaps in the feed. Nothing here bears on engine behaviour.

- 2026-06-13: A shift handover minuted a routine observation. Two alerts deduplicated to one case after the correlation pass ran.

- 2026-06-13: The collector owner noted a routine observation. The case queue sat slightly above its running mean, entirely from low-severity items. The desk confirmed no case impact.

- 2026-06-02: The SOC lead logged a routine observation. The on-call handover recorded nothing outstanding for the next shift. The thread was archived after review.

- 2026-06-10: An on-call engineer filed a routine observation. A responder asked for the previous window's export and was pointed at the archive. The desk confirmed no case impact.

- 2026-06-21: A weekly detection review logged a routine observation. One sensor's feed was replayed after a broker restart, producing no duplicates downstream.

- 2026-06-08: The forensics reviewer reviewed a routine observation. Storage headroom on the collector was reported comfortable for the quarter. No dissent was recorded.

- 2026-06-21: The SOC lead logged a routine observation. An account lockout was traced to a stale credential in a scheduled job, not an intrusion.

- 2026-06-06: An on-call engineer filed a routine observation. Storage headroom on the collector was reported comfortable for the quarter. Referred to the dated decisions and closed.

- 2026-06-03: The detection-engineering desk spot-checked a routine observation. Two alerts deduplicated to one case after the correlation pass ran. Nothing here bears on engine behaviour.

- 2026-06-26: The SOC lead raised and closed a routine observation. The case queue sat slightly above its running mean, entirely from low-severity items. Noted and closed.

- 2026-06-08: The detection-engineering desk noted a routine observation. An analyst asked whether a session had already been closed; it had, in the prior window. The thread was archived after review.
