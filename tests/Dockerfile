FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

# Verifier dependencies, baked in (no network at trial time). The submitted Go
# source is recompiled here, so the toolchain is verifier-side too; grading uses
# the stdlib plus pytest.
# Two network steps, retried separately rather than chained: when they shared one
# RUN, a flaky index fetch for pytest threw away a successful golang-go install
# and redid the whole thing on the next attempt.
RUN set -eu; \
    delay=5; \
    for attempt in 1 2 3 4; do \
        if apt-get -o Acquire::Retries=3 -o Acquire::http::Timeout=20 \
                -o Acquire::https::Timeout=20 update \
            && apt-get -o Acquire::Retries=3 -o Acquire::http::Timeout=20 \
                -o Acquire::https::Timeout=20 install -y --no-install-recommends golang-go; then \
            rm -rf /var/lib/apt/lists/*; \
            exit 0; \
        fi; \
        echo "apt attempt ${attempt} failed, retrying in ${delay}s" >&2; \
        rm -rf /var/lib/apt/lists/*; \
        sleep "${delay}"; \
        delay=$((delay * 2)); \
    done; \
    exit 1

RUN set -eu; \
    delay=5; \
    for attempt in 1 2 3 4; do \
        if pip install --no-cache-dir --timeout 30 --retries 3 \
                pytest==8.4.1 \
                pytest-json-ctrf==0.3.5; then \
            exit 0; \
        fi; \
        echo "pip attempt ${attempt} failed, retrying in ${delay}s" >&2; \
        sleep "${delay}"; \
        delay=$((delay * 2)); \
    done; \
    exit 1

# Landing directory for the declared artifact (/app) collected from the agent's
# environment. Its parent must exist in the verifier image before the copy.
RUN mkdir -p /app

# Verifier-execution isolation: the submitted program is run under the unprivileged uid 65534
# (nobody). setpriv (util-linux) drops privileges; a world-writable scratch area lets the
# candidate write only there. /tests (held-out fixtures) and the reward path stay root-owned
# and unreadable/unwritable to the candidate. setpriv ships in the base image, so no package
# install is needed here.
RUN mkdir -p /candidate-work \
    && chmod 1777 /candidate-work

WORKDIR /tests
COPY test_outputs.py /tests/test_outputs.py
COPY harness.py /tests/harness.py
COPY test.sh /tests/test.sh
COPY fixtures/ /tests/fixtures/

# Keep the held-out fixtures readable only by root, so the unprivileged candidate cannot read
# expected outputs even though it can be handed staged inputs.
# Closing the two directories is enough: without search permission on them
# nothing below can be reached by another uid.
RUN chmod 700 /tests /tests/fixtures
