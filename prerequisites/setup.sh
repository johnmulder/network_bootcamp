#!/bin/sh

set -eu

usage() {
    echo "usage: $0 [--check]" >&2
    exit 2
}

mode=install
if [ "${1:-}" = "--check" ]; then
    mode=check
    shift
fi
[ "$#" -eq 0 ] || usage

if [ "$(uname -s)" != "Darwin" ]; then
    echo "error: this course requires macOS" >&2
    exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
    echo "error: Homebrew is required; install it from https://brew.sh/" >&2
    exit 1
fi

formulae="python wireshark zeek jq iperf3"

if [ "$mode" = install ]; then
    set --
    for formula in $formulae; do
        brew list --versions "$formula" >/dev/null 2>&1 || set -- "$@" "$formula"
    done
    if [ "$#" -gt 0 ]; then
        brew install "$@"
    fi
fi

status=0
for command in tcpdump netstat route arp traceroute nc; do
    if command -v "$command" >/dev/null 2>&1; then
        printf '%-10s %s\n' "$command" "ok (macOS)"
    else
        printf '%-10s %s\n' "$command" "missing from macOS"
        status=1
    fi
done

for requirement in \
    "python:python3" \
    "wireshark:tshark" \
    "zeek:zeek" \
    "jq:jq" \
    "iperf3:iperf3"
do
    formula=${requirement%%:*}
    command=${requirement#*:}
    if brew list --versions "$formula" >/dev/null 2>&1 && \
        command -v "$command" >/dev/null 2>&1; then
        printf '%-10s %s\n' "$formula" "ok"
    else
        printf '%-10s %s\n' "$formula" "missing"
        status=1
    fi
done

if [ "$status" -eq 0 ]; then
    project_root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
    if [ "$mode" = install ]; then
        python3 "$project_root/labs/build_fixtures.py"
    else
        python3 "$project_root/labs/build_fixtures.py" --check
    fi
    echo "prerequisites ready"
    echo "next: ./course"
else
    echo "prerequisites incomplete; run $0" >&2
fi

exit "$status"
