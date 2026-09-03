# IPv6 and Neighbor Discovery

> **Module 1 · Section 3**

## Why It Matters

IPv6 changes address size and local-neighbor mechanisms while preserving the
core routed-packet model. Conceptual familiarity prevents IPv4-only reasoning
from causing blind spots.

## Core Model

* IPv6 uses 128-bit addresses and prefix lengths; `/64` is the common size for
  a LAN segment.

* Link-local addresses in `fe80::/10` support neighbor and router communication
  even without a global address.

* Neighbor Discovery uses ICMPv6 multicast messages instead of ARP broadcasts.

* Router Advertisements can provide prefix and default-router information;
  DHCPv6 can supply additional configuration depending on design.

* IPv6 has no router-based packet fragmentation; endpoints rely on Path MTU
  Discovery and source fragmentation when needed.

## Reasoning Process

1. Classify each IPv6 address as loopback, link-local, unique-local, multicast,
   or global.

2. Use the prefix to decide whether the destination is on-link.

3. Identify the Neighbor Solicitation, Neighbor Advertisement, and router
   information required.

4. Trace the packet while preserving scope identifiers for link-local
   addresses.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding
   touch work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/02-ipv6-and-neighbor-discovery.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **IPv6
   and Neighbor Discovery** in
   `work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/02-ipv6-and-neighbor-discovery.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,120p' labs/fixtures/routing/macos-routes.txt
   column -s, -t labs/fixtures/routing/route-candidates.csv
   jq '.' labs/fixtures/network/ipv6.json
   jq '.' labs/fixtures/routing/traceroute.json
   tshark -r labs/fixtures/pcaps/mtu-failure.pcap -Y 'tcp.options.mss || icmp' -T fields -E header=y -E separator=, -e frame.number -e ip.src -e ip.dst -e tcp.options.mss_val -e icmp.type -e icmp.code -e icmp.mtu
   ```

4. In the output file, add a `## Analysis` section for **IPv6 and Neighbor
   Discovery**. Apply the numbered Reasoning Process in order. For each step,
   cite at least one exact command result and label the statement as an
   observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* `10.0.20.40/32` wins for `10.0.20.40`, while the two equal OSPF `/24` routes
  are candidates for other addresses in `10.0.20.0/24`.

* The IPv6 host uses `fe80::1%en0` as its default router, and traceroute hop 3
  is unknown rather than proven absent from the path.

* The MTU capture advertises MSS 1460, sends a 1400-byte TCP payload, receives
  ICMP type 3 code 4 with MTU 1200, and retransmits the oversized segment.

## Completion Standard

Submit
`work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/02-ipv6-and-neighbor-discovery.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. What function replaces ARP in IPv6?

2. Why does a link-local address sometimes require an interface scope?

3. Which endpoint is responsible for IPv6 fragmentation?
