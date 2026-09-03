# Prerequisites

The course runs entirely on one Mac laptop. No second host, virtual machine,
container runtime, cloud account, proprietary analyzer, or enterprise network
access is required.

## Requirements

* macOS on Apple silicon or Intel
* A local administrator account for initial installation and optional packet
  capture
* Homebrew
* Internet access during initial installation

The course uses saved evidence whenever elevated access would otherwise be
required. Live exercises generate traffic only on the laptop's loopback
interface (`lo0`).

## Install

If Homebrew is not installed, install it using the instructions at
[brew.sh](https://brew.sh/). Then run:

```sh
cd /path/to/network_bootcamp
./prerequisites/setup.sh
```

The script is idempotent: it installs only missing packages and builds the
[local lab dataset](../labs/README.md). Verify the tools and fixture checksums
at any time with:

```sh
./prerequisites/setup.sh --check
```

## Installed Tools

| Tool | Course use | License |
| --- | --- | --- |
| Python | Local clients, servers, and fixture processing | Python-2.0 |
| TShark | Packet inspection and protocol decoding | GPL-2.0-or-later |
| Zeek | Protocol logs and network-security analysis | BSD-3-Clause |
| jq | JSON and structured-log analysis | MIT |
| iperf3 | Local TCP and UDP traffic generation | BSD-3-Clause |

Homebrew installs the command-line Wireshark formula for TShark; no GUI is
required. macOS already supplies open-source BSD networking utilities used by
the course, including `tcpdump`, `netstat`, `route`, `arp`, `traceroute`, and
`nc`.

## Packet Capture

Saved packet captures are the default and require no special permissions. When
a live loopback capture is useful, start it in one terminal:

```sh
sudo tcpdump -i lo0 -w /tmp/network-bootcamp.pcap
```

Generate the local traffic in another terminal, then press Control-C in the
capture terminal. Analyze the result without elevated privileges:

```sh
tshark -r /tmp/network-bootcamp.pcap
```

Never capture traffic belonging to other users or direct course traffic at a
system you do not control.

## Deliberate Exclusions

The setup does not install Docker Desktop, a virtual-machine platform, router
emulators, commercial packet analyzers, or vendor SDKs. Behaviors that require
multiple network devices—such as VLAN trunks, VRFs, OSPF/BGP adjacencies,
firewall failover, WAN routing, and OT segmentation—are studied through local
packet captures, route tables, logs, and diagrams.
