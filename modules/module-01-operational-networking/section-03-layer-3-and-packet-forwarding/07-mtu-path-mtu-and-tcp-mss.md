# MTU, Path MTU Discovery, and TCP MSS

> **Module 1 · Section 3**

## Why It Matters

Packet-size mismatches create failures where small exchanges succeed and large
ones stall. MTU, Path MTU Discovery, and TCP MSS operate at different points in
the problem.

## Core Model

* Interface MTU limits the IP packet size carried without link-layer
  fragmentation or an error.

* Path MTU is the smallest MTU across the complete path.

* IPv4 may fragment under defined conditions; IPv6 routers do not fragment
  forwarded packets.

* Path MTU Discovery relies on ICMP feedback or transport-layer probing to find
  a usable size.

* TCP MSS advertises the maximum TCP payload a receiver wants per segment and
  can be adjusted at boundaries to avoid oversized packets.

## Reasoning Process

1. Identify the packet size, headers, interface MTUs, and smallest path link.

2. Determine whether fragmentation is allowed and where it could occur.

3. Find the relevant ICMP feedback or its absence.

4. Relate the effective MSS to the path MTU and observed TCP retransmissions.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding
   touch work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/07-mtu-path-mtu-and-tcp-mss.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **MTU,
   Path MTU Discovery, and TCP MSS** in
   `work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/07-mtu-path-mtu-and-tcp-mss.md`.
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

4. In the output file, add a `## Analysis` section for **MTU, Path MTU
   Discovery, and TCP MSS**. Apply the numbered Reasoning Process in order. For
   each step, cite at least one exact command result and label the statement as
   an observation or interpretation.

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
`work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/07-mtu-path-mtu-and-tcp-mss.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can ping succeed while a large transfer fails?

2. How are MTU and TCP MSS related but not identical?

3. What is an ICMP black hole?
