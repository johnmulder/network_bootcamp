# Prerequisites

The course runs entirely on one Mac laptop. No second host, virtual machine,
container runtime, cloud account, proprietary analyzer, or enterprise network
access is required.

## Requirements

- macOS on Apple silicon or Intel
- a local administrator account for initial installation and optional packet
  capture
- Homebrew when installing missing or outdated tools
- internet access during initial installation

The core course reads local, saved evidence. It does not require `sudo`, create
connections to lab targets, or depend on another machine. Optional live
observations generate traffic only on the laptop's loopback interface (`lo0`).

## Install

If you need to install tools and Homebrew is not installed, follow the
instructions at [brew.sh](https://brew.sh/). Then run:

```sh
cd /path/to/network_bootcamp
./prerequisites/setup.sh
```

The script is idempotent: it installs packages only for missing commands and
verifies the committed
[local lab dataset](../labs/README.md). It can be run again safely after an
interrupted or partial installation. When setup succeeds, start with
`./course`.

The default installs only the one-day tools: Python, TShark, and jq. Python 3.10
or later is required; an older Python is queued for installation. If an older
system Python still takes precedence afterward, correct your shell's Homebrew
PATH setup and rerun the check. A readiness
check uses available commands and does not refresh Homebrew package metadata.
Existing usable installations are accepted even if their formula names differ.
Homebrew remains the installer for missing tools. Readiness checks do not need
Homebrew when the commands are already available. `./course doctor --json`
also checks representative jq operations and TShark fields.

Routine setup preserves saved evidence. Restore damaged fixtures from the
matching course copy; maintainers can deliberately regenerate them with
`python3 labs/build_fixtures.py`. Saved delivery sessions reject changed course
or evidence versions rather than mixing results from different versions.

For the optional Zeek and iperf3 reference exercises:

```sh
./prerequisites/setup.sh --extended
./prerequisites/setup.sh --check --extended
```

## Tool Roles

| Tool | Course role | Requirement | License |
| --- | --- | --- | --- |
| Python | Builds fixtures and runs all three workbenches | Core | Python-2.0 |
| TShark | Decodes saved packet captures and optional local captures | Core | GPL-2.0-or-later |
| Zeek | Produces and interprets network-security telemetry | Extended study | BSD-3-Clause |
| jq | Filters JSON fixtures and structured logs | Core | MIT |
| iperf3 | Generates TCP or UDP traffic for optional local experiments | Optional practice | BSD-3-Clause |
| macOS BSD tools | Inspect routes, neighbors, sockets, paths, and packet captures | Core and optional practice | Open source, included with macOS |

Homebrew installs the command-line Wireshark formula for TShark; no GUI is
required. `cat` and `column` support the core saved-evidence views. The setup
script reports macOS-provided `tcpdump`, `netstat`, `route`, `arp`, `traceroute`,
and `nc` separately; missing optional live tools do not block offline delivery.

## Verify the Current Project

From the repository root, check the tools, fixtures, and every interactive
workbench:

```sh
./prerequisites/setup.sh --check
./course verify
```

Both commands must exit successfully for the one-day route. Use `--extended`
when checking the additional reference tools. The course check reports 36 fixture
files and a passing self-test for each workbench. See the [lab dataset
guide](../labs/README.md) if a checksum or fixture path fails.

`markdownlint-cli2` is a maintainer convenience, not a course prerequisite and
is not installed by `setup.sh`.

## Optional Live Packet Capture

The saved packet captures are the reference evidence and require no special
permissions. If a guide calls for a live loopback observation, start a capture
in one terminal:

```sh
sudo tcpdump -i lo0 -w /tmp/network-bootcamp.pcap
```

Generate only the guide's local traffic in another terminal, then press
Control-C in the capture terminal. Analyze the result without elevated
privileges:

```sh
tshark -r /tmp/network-bootcamp.pcap
```

Never capture traffic belonging to other users or direct course traffic at a
system you do not control. Skip the live observation when capture is not
authorized; the saved fixture supports the same core learning objective.

## Deliberate Exclusions

The setup does not install Docker Desktop, a virtual-machine platform, router
emulators, commercial packet analyzers, or vendor SDKs. Behaviors that require
multiple network devices—such as VLAN trunks, VRFs, OSPF/BGP adjacencies,
firewall failover, WAN routing, and OT segmentation—are studied through local
packet captures, route tables, logs, and diagrams.
