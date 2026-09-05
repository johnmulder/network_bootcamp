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

requirements="python:python3 wireshark:tshark jq:jq"
if [ "$extended" = true ]; then
    requirements="$requirements zeek:zeek iperf3:iperf3"
fi

usable() {
    command -v "$1" >/dev/null 2>&1 || return 1
    if [ "$1" = python3 ]; then
        python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))'
    fi
}

if [ "$mode" = install ]; then
    set --
    for requirement in $requirements; do
        formula=${requirement%%:*}
        command=${requirement#*:}
        usable "$command" || set -- "$@" "$formula"
    done
    if [ "$#" -gt 0 ]; then
        if ! command -v brew >/dev/null 2>&1; then
            echo "error: Homebrew is required to install missing tools; see https://brew.sh/" >&2
            exit 1
        fi
        brew install "$@"
    fi
fi

status=0
for command in cat column; do
    if usable "$command"; then
        printf '%-10s %s\n' "$command" "ok (macOS)"
    else
        printf '%-10s %s\n' "$command" "missing from macOS"
        status=1
    fi
done

for command in tcpdump netstat route arp traceroute nc; do
    if usable "$command"; then
        printf '%-10s %s\n' "$command" "ok (optional live exercise)"
    else
        printf '%-10s %s\n' "$command" "unavailable (optional live exercise)"
    fi
done

for requirement in $requirements
do
    formula=${requirement%%:*}
    command=${requirement#*:}
    if usable "$command"; then
        printf '%-10s %s\n' "$formula" "ok"
    else
        printf '%-10s %s\n' "$formula" "missing or unusable (Python requires 3.10+)"
        status=1
    fi
done

if [ "$status" -eq 0 ]; then
    project_root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
    python3 "$project_root/labs/build_fixtures.py" --check
    echo "prerequisites ready"
    echo "next: ./course"
else
    echo "prerequisites incomplete; run $0" >&2
fi

exit "$status"
