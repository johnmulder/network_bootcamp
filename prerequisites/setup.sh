#!/bin/sh

set -eu

usage() {
    echo "usage: $0 [--check] [--extended]" >&2
    exit 2
}

mode=install
extended=false
while [ "$#" -gt 0 ]; do
    case "$1" in
        --check) mode=check ;;
        --extended) extended=true ;;
        *) usage ;;
    esac
    shift
done

if [ "$(uname -s)" != "Darwin" ]; then
    echo "error: this course requires macOS" >&2
    exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
    echo "error: Homebrew is required; install it from https://brew.sh/" >&2
    exit 1
fi

requirements="python:python3 wireshark:tshark jq:jq"
if [ "$extended" = true ]; then
    requirements="$requirements zeek:zeek iperf3:iperf3"
fi

if [ "$mode" = install ]; then
    set --
    for requirement in $requirements; do
        formula=${requirement%%:*}
        command=${requirement#*:}
        command -v "$command" >/dev/null 2>&1 || set -- "$@" "$formula"
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

for requirement in $requirements
do
    formula=${requirement%%:*}
    command=${requirement#*:}
    if command -v "$command" >/dev/null 2>&1; then
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
