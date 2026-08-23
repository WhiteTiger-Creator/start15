#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export GOCACHE=/tmp/gocache GO111MODULE=off GOPATH=/tmp/gopath

# --- Step 1: rebuild the authoritative event timeline (#IR-5170, #IR-5174) --
# The collector left /app/data/event_timeline.json holding a truncated prefix.
# Replay its journal onto the pre-truncation snapshot, carry each stamp onto the
# reference clock, and write the result back to that path.

go run "${SCRIPT_DIR}/recover_timeline.go"

# --- Step 2: restore the correlation engine and produce the triage artifacts --

cp "${SCRIPT_DIR}/correlate_incidents_fixed.go" /app/workflow/correlate_incidents.go
go run /app/workflow/correlate_incidents.go --output-dir /app/output
