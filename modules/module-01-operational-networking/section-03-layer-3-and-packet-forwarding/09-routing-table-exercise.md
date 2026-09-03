# Routing-Table Exercise

> **Module 1 · Section 3**

## Why It Matters

This exercise consolidates addressing, longest-prefix match, next-hop
resolution, ECMP, MTU, NAT, and return-path reasoning into one
packet-forwarding narrative.

## Core Model

* The selected route must be justified against every competing destination
  match.

* The next hop and egress interface must be resolved rather than copied without
  explanation.

* Forward and return decisions are independent and can use different tables or
  paths.

* Packet transformation and size constraints must be placed at specific
  boundaries.

* The final conclusion must cite the named table, diagram, or capture
  supporting each step.

## Reasoning Process

1. Normalize endpoint addresses, prefixes, routing contexts, and destination
   tuple.

2. Resolve the forward path one table at a time, including recursive next hops.

3. Apply translation, policy, and MTU effects at their modeled boundaries.

4. Repeat from the destination for the return direction and identify asymmetry.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding
   touch work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/09-routing-table-exercise.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Routing-Table Exercise** in
   `work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/09-routing-table-exercise.md`.
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

4. In the output file, add a `## Analysis` section for **Routing-Table
   Exercise**. Apply the numbered Reasoning Process in order. For each step,
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
`work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/09-routing-table-exercise.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Did you explain why less-specific routes lost?

2. Did you confirm reachability of every recursive next hop?

3. Did you trace the return path instead of mirroring the forward path?
