# IPv4 Addressing, CIDR, and Subnets

> **Module 1 · Section 3**

## Why It Matters

Address and prefix interpretation determines whether a destination is local,
which route can match it, and how designs divide broadcast and routing domains.

## Core Model

* An IPv4 address identifies an interface; the prefix length identifies the
  network portion used for on-link and routing decisions.

* CIDR expresses contiguous prefix bits and supports variable-size networks and
  route aggregation.

* Network and broadcast addresses have special meaning in conventional IPv4
  subnets, while usable host ranges lie between them.

* Nested destination routes are normal: `10.0.20.40/32` overlaps its covering
  `10.0.20.0/24` and `10.0.0.0/8`. Longest-prefix matching selects the most
  specific installed match. Conflicting address assignments are a separate
  design problem; overlapping routes do not make a table malformed.

* Address membership is a binary prefix comparison, not a visual comparison of
  decimal octets.

## Reasoning Process

1. Convert the prefix length into a mask or reason directly in binary.

2. Calculate the network boundary and address range.

3. Test whether source, destination, and gateway belong to the expected subnet.

4. Identify whether a host should use direct delivery or a gateway.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding
   touch work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/01-addressing-cidr-and-subnets.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **IPv4
   Addressing, CIDR, and Subnets** in
   `work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/01-addressing-cidr-and-subnets.md`.
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

4. In the output file, add a `## Analysis` section for **IPv4 Addressing, CIDR,
   and Subnets**. Apply the numbered Reasoning Process in order. For each step,
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
`work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/01-addressing-cidr-and-subnets.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why are `192.0.2.1/24` and `192.0.2.1/25` different forwarding statements?

2. How does route aggregation reduce routing-table size?

3. What happens when a configured gateway is outside the host's on-link prefix?

## Sources

Reviewed September 14, 2026. Exercises remain usable offline.

[RFC 1812 §5.2.4.3](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3):
longest matching destination prefix.
