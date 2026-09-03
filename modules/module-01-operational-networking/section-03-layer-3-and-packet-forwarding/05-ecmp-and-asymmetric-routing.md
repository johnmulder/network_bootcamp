# ECMP and Asymmetric Routing

> **Module 1 · Section 3**

## Why It Matters

Equal-cost multipath can improve capacity and resilience, but it also creates
path diversity. Forward and return traffic may encounter different devices,
state, and telemetry.

## Core Model

* ECMP installs multiple next hops for one prefix when route attributes and
  costs are eligible.

* Forwarding usually hashes flow fields so packets in one flow remain on one
  path.

* Asymmetric routing means the reverse direction follows a different device
  sequence, not necessarily that connectivity is broken.

* Stateless routers tolerate asymmetry, while stateful firewalls, NAT, and some
  monitoring designs may not.

* Captures from one path can show only one direction and create a false
  impression of missing traffic.

## Reasoning Process

1. Enumerate all eligible forward and return next hops.

2. Identify the hash fields and any middleboxes on each possible path.

3. Mark state that must be shared or synchronized across devices.

4. Compare capture coverage with the possible path set before declaring traffic
   absent.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding
   touch work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/05-ecmp-and-asymmetric-routing.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **ECMP
   and Asymmetric Routing** in
   `work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/05-ecmp-and-asymmetric-routing.md`.
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

4. In the output file, add a `## Analysis` section for **ECMP and Asymmetric
   Routing**. Apply the numbered Reasoning Process in order. For each step, cite
   at least one exact command result and label the statement as an observation
   or interpretation.

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
`work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/05-ecmp-and-asymmetric-routing.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why does ECMP not imply per-packet load balancing?

2. When is asymmetric routing harmless?

3. How can path asymmetry produce an apparent one-sided PCAP?
