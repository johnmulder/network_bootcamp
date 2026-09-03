# Longest Prefix, Next Hop, and Default Routes

> **Module 1 · Section 3**

## Why It Matters

Route choice is primarily a two-stage problem: choose the most-specific
destination prefix, then choose among routes to that prefix using protocol
preference and metric.

## Core Model

* Longest-prefix match compares prefix length among all destination matches,
  regardless of which protocol installed them.

* Administrative preference or distance normally compares routes only after
  destination-prefix specificity is equal.

* Metrics compare paths within a routing protocol and are not inherently
  comparable across protocols.

* A default route is a zero-length prefix and therefore the least-specific
  possible match.

* Recursive resolution can make the installed forwarding path depend on another
  route to the advertised next hop.

## Reasoning Process

1. List matching routes and eliminate every route with a shorter prefix than
   the best match.

2. Among equal prefixes, apply route-source preference.

3. Compare metrics or multipath eligibility within the preferred source.

4. Resolve the chosen next hop until an egress interface is known.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding
   touch work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/04-longest-prefix-next-hop-and-default-routes.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Longest Prefix, Next Hop, and Default Routes** in
   `work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/04-longest-prefix-next-hop-and-default-routes.md`.
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

4. In the output file, add a `## Analysis` section for **Longest Prefix, Next
   Hop, and Default Routes**. Apply the numbered Reasoning Process in order. For
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
`work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/04-longest-prefix-next-hop-and-default-routes.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can a `/32` route override a default route with a better metric?

2. When is administrative preference relevant?

3. What new failure can recursive next-hop resolution introduce?
