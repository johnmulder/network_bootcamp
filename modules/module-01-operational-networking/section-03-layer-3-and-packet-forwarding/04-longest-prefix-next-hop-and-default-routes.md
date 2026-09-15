# Longest Prefix, Next Hop, and Default Routes

> **Module 1 · Section 3**

## Why It Matters

Separate route installation from packet forwarding. The control plane selects
paths for each prefix; the forwarding plane looks up a packet destination in
the installed table. It does not rerun routing protocols for every packet.

## Core Model

* Longest-prefix match compares prefix length among all destination matches,
  regardless of which protocol installed them.

* Administrative preference or distance helps select which source installs
  a route for the same prefix. A preferred default does not displace an
  installed, matching host route during forwarding.

* Metrics compare paths within a routing protocol and are not inherently
  comparable across protocols.

* A default route is a zero-length prefix and therefore the least-specific
  possible match.

* Recursive resolution can make the installed forwarding path depend on another
  route to the advertised next hop.

## Reasoning Process

1. Identify the routing context and whether the input is a candidate list
   or an installed forwarding table.

2. For candidates, select paths for each identical prefix using the modeled
   source preference, metric, and multipath rules. Protocols have their own
   selection procedures; this CSV is a simplified model.

3. For a packet, select the longest matching prefix in the resulting table.

4. Resolve the selected next hop and egress adjacency. An installed route
   alone does not establish neighbor resolution or successful delivery.

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
   tshark -r labs/fixtures/pcaps/mtu-failure.pcap -Y 'tcp || icmp' -T fields -E header=y -E separator=, -e frame.number -e ip.src -e ip.dst -e ip.len -e ip.hdr_len -e tcp.hdr_len -e tcp.len -e tcp.seq -e tcp.options.mss_val -e icmp.type -e icmp.code -e icmp.mtu
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

## Sources

Reviewed September 14, 2026. Exercises remain usable offline.

[RFC 1812 §5.2.4.3](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3):
route selection and forwarding.
