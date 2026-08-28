FROM public.ecr.aws/docker/library/golang:1.24-bookworm@sha256:1a6d4452c65dea36aac2e2d606b01b4a029ec90cc1ae53890540ce6173ea77ac

ENV DEBIAN_FRONTEND=noninteractive

# The task is Go-only, so the canonical Go image carries the toolchain
# rather than a Python base with golang-go bolted on.
ENV GOCACHE=/tmp/gocache \
    GOPATH=/tmp/gopath \
    GO111MODULE=off

# Least-volatile layers first: fix the working directory before the apt and
# dependency layers so a change to those never invalidates the WORKDIR layer.
WORKDIR /app

# This build's only network step, and a transient mirror failure here voids a
# whole grading trial. Two layers of retry: Acquire::Retries retries each
# individual download, and the loop retries the whole transaction after clearing
# the partial lists a failed update leaves behind. The timeouts are explicit so a
# mirror that hangs rather than refuses cannot eat the build budget.
RUN set -eu; \
    delay=5; \
    for attempt in 1 2 3 4 5 6; do \
        if apt-get -o Acquire::Retries=5 -o Acquire::http::Timeout=30 \
                -o Acquire::https::Timeout=30 update \
            && apt-get -o Acquire::Retries=5 -o Acquire::http::Timeout=30 \
                -o Acquire::https::Timeout=30 install -y --no-install-recommends \
                tmux asciinema; then \
            rm -rf /var/lib/apt/lists/*; \
            exit 0; \
        fi; \
        echo "apt attempt ${attempt} failed, retrying in ${delay}s" >&2; \
        rm -rf /var/lib/apt/lists/*; \
        sleep "${delay}"; \
        if [ "${delay}" -lt 60 ]; then delay=$((delay * 2)); fi; \
    done; \
    exit 1

# /app/data/event_timeline.json ships TRUNCATED exactly as the collector left it;
# the pre-truncation snapshot, the collector journal and the sensor registry
# beside it are the recovery sources. All values are synthetic.
COPY app/ /app/

# The default output directory the contract names. instruction.md tells the
# solver it already exists when a run starts and that the engine may write
# only inside the directory it is given, which was not true of the shipped
# image: a no-argument run had to create it, and the graded run is
# unprivileged. It is created here, writable, so the promise holds.
RUN mkdir -p /app/output && chmod 1777 /app/output
RUN cp /app/workflow/correlate_incidents.go /app/workflow/.correlate_incidents.original.go \
    && chmod a-w /app/workflow/.correlate_incidents.original.go
