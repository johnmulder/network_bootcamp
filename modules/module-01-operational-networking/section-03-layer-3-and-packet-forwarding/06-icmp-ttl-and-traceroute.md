# ICMP, TTL, and Traceroute

> **Module 1 · Section 3**

## Why It Matters

ICMP reports network-layer conditions and supports diagnostics. TTL or Hop
Limit prevents persistent loops, while traceroute turns expiration messages
into a partial path view.

## Core Model

* IPv4 TTL and IPv6 Hop Limit are decremented by each router; expiration
  normally causes an ICMP time-exceeded message.

* ICMP also reports unreachable destinations, fragmentation needs, and other
  control information.

* Traceroute sends probes with increasing TTL or Hop Limit and records
  responding devices.

* Responses can be filtered, rate-limited, sourced from unexpected interfaces,
  or follow a different return path.

* A traceroute result is evidence about probe and response behavior, not a
  complete proof of the application path.

## Reasoning Process

1. Identify the traceroute probe type, destination port or identifier, and
   increasing lifetime.

2. Map each response to the probe that triggered it.

3. Account for missing, repeated, or load-balanced hops.

4. Compare traceroute with routing and application evidence before reaching a
   conclusion.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding
   touch work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/06-icmp-ttl-and-traceroute.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **ICMP,
   TTL, and Traceroute** in
   `work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/06-icmp-ttl-and-traceroute.md`.
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

4. In the output file, add a `## Analysis` section for **ICMP, TTL, and
   Traceroute**. Apply the numbered Reasoning Process in order. For each step,
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
`work/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/06-icmp-ttl-and-traceroute.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can a router forward application traffic but not appear in traceroute?

2. Does the source address of an ICMP reply always identify the traversed
   interface?

3. What does an asterisk in traceroute actually prove?
