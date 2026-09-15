# MTU, Path MTU Discovery, and TCP MSS

> **Module 1 · Section 3**

## Why It Matters

Packet-size mismatches create failures where small exchanges succeed and large
ones stall. MTU, Path MTU Discovery, and TCP MSS operate at different points in
the problem.

## Core Model

* Interface IP MTU limits the IP packet size carried without IP
  fragmentation; exceeding it can require fragmentation or an error/drop.

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

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the largest TCP payload with a 1200-byte path
limit and two 20-byte headers.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/mtu-failure.pcap -Y 'tcp || icmp' -T fields -E header=y -e frame.number -e ip.len -e ip.hdr_len -e tcp.hdr_len -e tcp.len -e tcp.seq -e tcp.options.mss_val -e icmp.type -e icmp.code -e icmp.mtu
```

## Expected Evidence and Worked Reasoning

The bound is 1160 bytes. The trace shows a 1400-byte payload and ICMP type 3
code 4 reporting 1200, followed by a repeated sequence. Endpoint receipt of
ICMP is not demonstrated.

## Completion Standard

Show arithmetic, repeated sequence, and the capture-location limit.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can ping succeed while a large transfer fails?

2. How are MTU and TCP MSS related but not identical?

3. What is an ICMP black hole?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1191 §3 — path MTU discovery](https://www.rfc-editor.org/rfc/rfc1191.html#section-3)

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
