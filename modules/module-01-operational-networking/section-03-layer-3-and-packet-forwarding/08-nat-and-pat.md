# NAT and PAT

> **Module 1 · Section 3**

## Why It Matters

Address and port translation changes observable identities across a boundary.
Investigations must track both sides of the mapping and the state that connects
them.

## Core Model

* Source NAT rewrites the source address, destination NAT rewrites the
  destination, and PAT also translates transport ports.

* A translation normally creates state keyed by protocol and endpoint tuples.

* Inside-local, inside-global, outside-local, and outside-global terminology
  describes viewpoints but varies across vendors.

* NAT does not inherently provide security; policy and stateful filtering are
  separate decisions even when implemented on one device.

* Logs must include mapping, timestamps, protocol, and ideally rule or device
  context to attribute translated traffic.

## Reasoning Process

1. Write the tuple before translation and the tuple after translation.

2. Identify which direction creates state and how return traffic matches it.

3. Mark where captures or logs observe each tuple.

4. Check expiry, port reuse, hairpin behavior, and asymmetric-path risks.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding
   touch work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/08-nat-and-pat.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **NAT
   and PAT** in
   `work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/08-nat-and-pat.md`.
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

4. In the output file, add a `## Analysis` section for **NAT and PAT**. Apply
   the numbered Reasoning Process in order. For each step, cite at least one
   exact command result and label the statement as an observation or
   interpretation.

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
`work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/08-nat-and-pat.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why is an external translated address insufficient to identify an internal
   host?

2. Can NAT occur without a firewall permit?

3. What evidence is required when translated ports are reused over time?
