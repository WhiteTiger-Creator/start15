# Planning governance log

How the incident-correlation engine is *meant* to behave -- the recovery of the truncated event timeline, the clock correction, the basis for every boundary, action severity, chain formation and the handling of an oversized chain -- was settled incrementally by the incident-response board, and those decisions live in the review entries below, not in any single summary. Several stages deliberately DEVIATE from the intuitive reading: a sensor's offset is added rather than subtracted, boundaries are drawn on the corrected stamp rather than the recorded one, a chain carries its worst action's severity rather than the sum, and an oversized chain is cut rather than reported whole. The February draft proposals were revisited during the 2026-05 response review and several were reversed; where a draft or interim conflicts with a later decision, the later dated decision governs. `/app/docs/triage_contract.json` is the output contract only.

- 2026-02-07: Response stand-up recorded a routine note against the estate asset inventory for window 1003. The triage backlog was cleared with no amendment raised.

> **Recovery draft proposal (2026-02-07 - #IR-5020)** Rosa: rebuild the truncated timeline by concatenating the pre-truncation snapshot with the collector journal and keeping the last row seen for each event id; a restored event is re-read from the snapshot *(Superseded -- reversed in the 2026-05 response review.)*

> **Recovery draft proposal (2026-02-14 - #IR-5026)** Anders: a sensor's recorded clock offset is SUBTRACTED from the observed stamp to reach the reference clock *(Superseded -- reversed in the 2026-05 response review.)*

> **Recovery draft proposal (2026-02-20 - #IR-5032)** Marek: session and window boundaries are drawn on the stamp the sensor recorded, since that is the figure the analyst sees in the console *(Superseded -- reversed in the 2026-05 response review.)*

- 2026-02-09: Detection desk noted dropped batches from the estate asset inventory in window 1004. Raised with the platform owner; the triage parameters were not touched.

- 2026-02-09: Response stand-up recorded a routine note against the estate asset inventory for window 1006. The triage backlog was cleared with no amendment raised.

- 2026-02-07: Analyst on duty logged a routine observation for the estate asset inventory during review window 1007. Alert-volume drift reviewed; no policy change requested.

- 2026-02-20: Detection desk noted dropped batches from the syslog relay in window 1008. Raised with the platform owner; the triage parameters were not touched.

- 2026-02-13: Analyst on duty logged a routine observation for the EDR collector during review window 1009. Alert-volume drift reviewed; no policy change requested.

- 2026-02-15: Post-incident review of the estate asset inventory in window 1012 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-02-21: Detection desk noted dropped batches from the syslog relay in window 1014. Raised with the platform owner; the triage parameters were not touched.

- 2026-02-20: Analyst on duty logged a routine observation for the syslog relay during review window 1017. Alert-volume drift reviewed; no policy change requested.

- 2026-02-06: Analyst on duty logged a routine observation for the estate asset inventory during review window 1018. Alert-volume drift reviewed; no policy change requested.

- 2026-02-09: Analyst on duty logged a routine observation for the estate asset inventory during review window 1020. Alert-volume drift reviewed; no policy change requested.

- 2026-02-22: Post-incident review of the estate asset inventory in window 1021 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-02-23: Response stand-up recorded a routine note against the estate asset inventory for window 1022. The triage backlog was cleared with no amendment raised.

- 2026-02-09: Post-incident review of the EDR collector in window 1023 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-02-04: Response stand-up recorded a routine note against the auth log shipper for window 1026. The triage backlog was cleared with no amendment raised.

- 2026-02-19: Analyst on duty logged a routine observation for the syslog relay during review window 1028. Alert-volume drift reviewed; no policy change requested.

- 2026-02-15: Response stand-up recorded a routine note against the EDR collector for window 1030. The triage backlog was cleared with no amendment raised.

- 2026-02-09: Post-incident review of the syslog relay in window 1033 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-02-13: Response stand-up recorded a routine note against the auth log shipper for window 1035. The triage backlog was cleared with no amendment raised.

- 2026-02-12: Post-incident review of the auth log shipper in window 1037 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-02-02: Detection desk noted dropped batches from the auth log shipper in window 1039. Raised with the platform owner; the triage parameters were not touched.

- 2026-02-10: Post-incident review of the estate asset inventory in window 1041 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-19: Response stand-up recorded a routine note against the estate asset inventory for window 1043. The triage backlog was cleared with no amendment raised.

> **Interim decision (2026-03-06 - #IR-5044)** Priya: a chain carries the SUM of the severities of the actions observed along it *(Revised -- see the 2026-05 response review.)*

- 2026-03-06: Response stand-up recorded a routine note against the EDR collector for window 1045. The triage backlog was cleared with no amendment raised.

- 2026-03-27: Response stand-up recorded a routine note against the estate asset inventory for window 1046. The triage backlog was cleared with no amendment raised.

- 2026-03-03: Analyst on duty logged a routine observation for the EDR collector during review window 1048. Alert-volume drift reviewed; no policy change requested.

- 2026-03-08: Analyst on duty logged a routine observation for the estate asset inventory during review window 1050. Alert-volume drift reviewed; no policy change requested.

- 2026-03-23: Response stand-up recorded a routine note against the auth log shipper for window 1053. The triage backlog was cleared with no amendment raised.

- 2026-03-14: Post-incident review of the auth log shipper in window 1056 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-21: Analyst on duty logged a routine observation for the estate asset inventory during review window 1058. Alert-volume drift reviewed; no policy change requested.

- 2026-03-17: Response stand-up recorded a routine note against the netflow tap for window 1061. The triage backlog was cleared with no amendment raised.

- 2026-03-17: Analyst on duty logged a routine observation for the auth log shipper during review window 1063. Alert-volume drift reviewed; no policy change requested.

- 2026-03-25: Response stand-up recorded a routine note against the syslog relay for window 1066. The triage backlog was cleared with no amendment raised.

- 2026-03-13: Post-incident review of the estate asset inventory in window 1069 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-16: Post-incident review of the EDR collector in window 1072 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-10: Detection desk noted dropped batches from the netflow tap in window 1073. Raised with the platform owner; the triage parameters were not touched.

- 2026-03-25: Response stand-up recorded a routine note against the estate asset inventory for window 1075. The triage backlog was cleared with no amendment raised.

- 2026-03-15: Response stand-up recorded a routine note against the estate asset inventory for window 1078. The triage backlog was cleared with no amendment raised.

- 2026-03-01: Response stand-up recorded a routine note against the netflow tap for window 1079. The triage backlog was cleared with no amendment raised.

- 2026-03-22: Detection desk noted dropped batches from the netflow tap in window 1081. Raised with the platform owner; the triage parameters were not touched.

- 2026-03-24: Response stand-up recorded a routine note against the syslog relay for window 1083. The triage backlog was cleared with no amendment raised.

- 2026-03-07: Analyst on duty logged a routine observation for the syslog relay during review window 1085. Alert-volume drift reviewed; no policy change requested.

- 2026-03-07: Post-incident review of the syslog relay in window 1088 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-08: Post-incident review of the netflow tap in window 1090 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-18: Post-incident review of the netflow tap in window 1092 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-17: Response stand-up recorded a routine note against the estate asset inventory for window 1094. The triage backlog was cleared with no amendment raised.

- 2026-04-03: Post-incident review of the auth log shipper in window 1095 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-22: Detection desk noted dropped batches from the EDR collector in window 1098. Raised with the platform owner; the triage parameters were not touched.

- 2026-04-13: Analyst on duty logged a routine observation for the syslog relay during review window 1099. Alert-volume drift reviewed; no policy change requested.

- 2026-04-01: Analyst on duty logged a routine observation for the estate asset inventory during review window 1100. Alert-volume drift reviewed; no policy change requested.

- 2026-04-22: Detection desk noted dropped batches from the netflow tap in window 1101. Raised with the platform owner; the triage parameters were not touched.

- 2026-04-06: Post-incident review of the estate asset inventory in window 1104 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-03: Post-incident review of the netflow tap in window 1106 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-17: Response stand-up recorded a routine note against the estate asset inventory for window 1109. The triage backlog was cleared with no amendment raised.

- 2026-04-27: Post-incident review of the estate asset inventory in window 1110 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-24: Response stand-up recorded a routine note against the EDR collector for window 1111. The triage backlog was cleared with no amendment raised.

- 2026-04-14: Detection desk noted dropped batches from the netflow tap in window 1113. Raised with the platform owner; the triage parameters were not touched.

- 2026-04-17: Post-incident review of the auth log shipper in window 1114 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-04: Post-incident review of the syslog relay in window 1117 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-23: Detection desk noted dropped batches from the EDR collector in window 1120. Raised with the platform owner; the triage parameters were not touched.

- 2026-04-13: Post-incident review of the syslog relay in window 1122 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-15: Analyst on duty logged a routine observation for the netflow tap during review window 1123. Alert-volume drift reviewed; no policy change requested.

- 2026-04-11: Analyst on duty logged a routine observation for the auth log shipper during review window 1125. Alert-volume drift reviewed; no policy change requested.

- 2026-05-02: Detection desk noted dropped batches from the estate asset inventory in window 1127. Raised with the platform owner; the triage parameters were not touched.

> **Governance decision (2026-05-05 - #IR-5150)** Priya: Input paths, final. The triage policy is always read from its fixed absolute path under /app/data; `--input` selects the event timeline only. Both `--input` and `--output-dir` keep their documented defaults.

> **Governance decision (2026-05-08 - #IR-5170)** Yusuf: Timeline recovery, final (supersedes #IR-5020). Start from the pre-truncation snapshot and replay the collector journal in ascending `seq`, never in file order. An `amend` overwrites the named field in place. A `retract` takes the event out of the timeline, but the collector keeps it as it stood at that moment. A `restore` puts a retracted event back EXACTLY as it stood when it was retracted: amendments posted before the retraction survive, and any amendment posted while it was out is lost. A change naming an event the snapshot never carried is ignored, and a restore of an event that was never retracted does nothing.

> **Governance decision (2026-05-11 - #IR-5174)** Yusuf: Clock correction, final (supersedes #IR-5026; deviates from the subtract reading). Each event carries a corrected stamp reached by ADDING its sensor's recorded `clock_offset_sec` to the observed stamp. An event whose sensor the registry does not list keeps its observed stamp as its corrected stamp.

> **Governance decision (2026-05-13 - #IR-5178)** Lena: Recovered shape, final. The rebuilt timeline is a JSON array ascending by corrected stamp and, on a tie, by `event_id`. Each record carries the eight declared fields -- the collector's bookkeeping (`seq`, `kind`, `posted_by`) never survives the replay.

> **Governance decision (2026-05-16 - #IR-5182)** Lena: Boundary basis, final (supersedes #IR-5032). Every boundary in this procedure -- the session gap and the chain window alike -- is measured on the CORRECTED stamp and never on the stamp the sensor recorded. A session opens on a host for an account whenever the gap from that account's previous event on that host exceeds the policy's `session_gap_sec`.

> **Governance decision (2026-05-19 - #IR-5186)** Marek: Action severity, final. The board fixes the severity of an observed action at: logon 5; logon_failed 8; process_start 10; net_connect 12; file_write 15; share_mount 20; priv_escalate 45; log_cleared 50. An action this table does not name contributes nothing.

> **Governance decision (2026-05-24 - #IR-5192)** Marek: Chain identity, final. A chain's `chain_id` is its account, a single colon, and the `event_id` of the earliest event on the chain in the #IR-5182 corrected-stamp order, written `account:event_id` with no spaces. The identifier is formed BEFORE the #IR-5194 host cap truncates anything, so a chain that loses hosts to the cap keeps the identifier it already had, and every `chain_truncated` row the cap queues carries that same identifier alongside the host it dropped.

> **Governance decision (2026-05-22 - #IR-5188)** Marek: Chain severity, final (revises #IR-5044; deviates from the summing interim). A chain carries the severity of its single worst action, not the sum of the actions observed along it. A chain whose severity falls below the policy's `severity_floor` is not reported as an incident and is queued as `below_floor` instead. That queue row names the chain's FIRST host in first-seen order, the same host the chain would have reported first, and one row is queued per chain rather than one per host.

> **Governance decision (2026-05-25 - #IR-5190)** Priya: Chain formation, final. An account's events are taken in corrected order and a run closes as soon as the next event lies further than the policy's `chain_window_sec` from the one before it, so the window slides with the activity rather than sitting in fixed buckets. A run is a chain candidate only where it touches at least `pivot_min_hosts` distinct hosts.

> **Governance decision (2026-05-28 - #IR-5194)** Yusuf: Oversized chains, final. A candidate reaching further than `max_chain_hosts` distinct hosts is cut at that many, keeping the hosts in the order they were first seen; every host beyond the cut is queued as `chain_truncated` and the events on those hosts take no part in the chain's severity, its span, its event count or the list of actions it reports: the chain is read as though the hosts beyond the cut were never on it. The severity a `chain_truncated` row carries is that same cut-down chain severity, one row per dropped host, so every row the cap queues for one chain carries the same severity as the chain itself. None of this reaches the run summary, whose `event_count` and `host_count` count the events read and the distinct hosts among them across the whole file, whether or not a cap later dropped a host from a chain.

> **Governance decision (2026-05-30 - #IR-5196)** Lena: Emission order, final. A chain is identified by its account and the event id it opens on. Chains are reported worst severity first, then earliest first stamp, then by chain id. The triage queue is worst severity first, then by chain id, then by host.

- 2026-05-09: Post-incident review of the auth log shipper in window 1130 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-18: Response stand-up recorded a routine note against the estate asset inventory for window 1132. The triage backlog was cleared with no amendment raised.

- 2026-05-07: Detection desk noted dropped batches from the auth log shipper in window 1135. Raised with the platform owner; the triage parameters were not touched.

- 2026-05-02: Response stand-up recorded a routine note against the EDR collector for window 1136. The triage backlog was cleared with no amendment raised.

- 2026-05-17: Response stand-up recorded a routine note against the syslog relay for window 1138. The triage backlog was cleared with no amendment raised.

- 2026-05-02: Analyst on duty logged a routine observation for the EDR collector during review window 1139. Alert-volume drift reviewed; no policy change requested.

- 2026-05-27: Post-incident review of the auth log shipper in window 1140 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-25: Analyst on duty logged a routine observation for the netflow tap during review window 1143. Alert-volume drift reviewed; no policy change requested.

- 2026-05-19: Detection desk noted dropped batches from the EDR collector in window 1145. Raised with the platform owner; the triage parameters were not touched.

- 2026-05-14: Analyst on duty logged a routine observation for the netflow tap during review window 1148. Alert-volume drift reviewed; no policy change requested.

- 2026-05-06: Analyst on duty logged a routine observation for the auth log shipper during review window 1149. Alert-volume drift reviewed; no policy change requested.

- 2026-05-20: Detection desk noted dropped batches from the syslog relay in window 1152. Raised with the platform owner; the triage parameters were not touched.

- 2026-05-07: Analyst on duty logged a routine observation for the EDR collector during review window 1154. Alert-volume drift reviewed; no policy change requested.

- 2026-05-11: Post-incident review of the syslog relay in window 1155 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-09: Post-incident review of the syslog relay in window 1156 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-06: Detection desk noted dropped batches from the auth log shipper in window 1158. Raised with the platform owner; the triage parameters were not touched.

- 2026-05-11: Post-incident review of the netflow tap in window 1160 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-11: Post-incident review of the estate asset inventory in window 1161 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-19: Analyst on duty logged a routine observation for the estate asset inventory during review window 1164. Alert-volume drift reviewed; no policy change requested.

- 2026-06-21: Detection desk noted dropped batches from the syslog relay in window 1167. Raised with the platform owner; the triage parameters were not touched.

> **Governance decision (2026-06-04 - #IR-5210)** Priya: Triage policy baseline, read from /app/data/triage_policy.json at that fixed absolute path. Any field the policy file omits keeps its baseline: session_gap_sec = 1800; pivot_min_hosts = 3; severity_floor = 40; chain_window_sec = 7200; max_chain_hosts = 12.

- 2026-06-21: Post-incident review of the estate asset inventory in window 1169 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-03: Response stand-up recorded a routine note against the estate asset inventory for window 1171. The triage backlog was cleared with no amendment raised.

- 2026-06-02: Detection desk noted dropped batches from the estate asset inventory in window 1174. Raised with the platform owner; the triage parameters were not touched.

- 2026-06-18: Analyst on duty logged a routine observation for the syslog relay during review window 1175. Alert-volume drift reviewed; no policy change requested.

- 2026-06-17: Detection desk noted dropped batches from the auth log shipper in window 1177. Raised with the platform owner; the triage parameters were not touched.

- 2026-06-02: Response stand-up recorded a routine note against the auth log shipper for window 1180. The triage backlog was cleared with no amendment raised.

- 2026-06-24: Response stand-up recorded a routine note against the estate asset inventory for window 1181. The triage backlog was cleared with no amendment raised.

- 2026-06-02: Analyst on duty logged a routine observation for the auth log shipper during review window 1182. Alert-volume drift reviewed; no policy change requested.

- 2026-06-12: Post-incident review of the syslog relay in window 1184 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-18: Post-incident review of the EDR collector in window 1187 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-23: Analyst on duty logged a routine observation for the netflow tap during review window 1189. Alert-volume drift reviewed; no policy change requested.

- 2026-06-13: Response stand-up recorded a routine note against the syslog relay for window 1191. The triage backlog was cleared with no amendment raised.

- 2026-06-13: Response stand-up recorded a routine note against the estate asset inventory for window 1194. The triage backlog was cleared with no amendment raised.

- 2026-06-02: Analyst on duty logged a routine observation for the EDR collector during review window 1196. Alert-volume drift reviewed; no policy change requested.

- 2026-06-10: Detection desk noted dropped batches from the auth log shipper in window 1198. Raised with the platform owner; the triage parameters were not touched.

- 2026-06-21: Response stand-up recorded a routine note against the netflow tap for window 1199. The triage backlog was cleared with no amendment raised.

- 2026-06-08: Response stand-up recorded a routine note against the auth log shipper for window 1202. The triage backlog was cleared with no amendment raised.

- 2026-06-21: Detection desk noted dropped batches from the syslog relay in window 1205. Raised with the platform owner; the triage parameters were not touched.

- 2026-06-06: Post-incident review of the estate asset inventory in window 1207 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-03: Detection desk noted dropped batches from the EDR collector in window 1210. Raised with the platform owner; the triage parameters were not touched.

- 2026-06-26: Post-incident review of the estate asset inventory in window 1212 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-08: Post-incident review of the EDR collector in window 1214 closed with no action; the standing thresholds were reconfirmed as they are.
