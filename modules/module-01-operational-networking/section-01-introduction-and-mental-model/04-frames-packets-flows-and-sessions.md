# Frames, Packets, Flows, and Sessions

> **Module 1 · Section 1**

## Why It Matters

These terms describe different views of communication. Correctly choosing the
unit of analysis prevents errors such as treating a Layer 2 destination as an
end-to-end destination.

## Core Model

* A frame is a link-local delivery unit with Layer 2 source and destination
  addresses. It is normally replaced at each routed hop.

* An IP packet carries end-to-end network-layer addresses, although NAT can
  rewrite them at a boundary.

* A transport segment or datagram carries ports and protocol state used by
  applications.

* A flow is an analytical grouping, commonly identified by source and
  destination addresses, ports, and transport protocol.

* A session is maintained state. Its definition depends on the endpoint,
  firewall, proxy, VPN, or monitoring tool observing it.

## Reasoning Process

1. Select one captured communication and identify its frame, packet, transport,
   flow, and session representations.

2. Mark which identifiers remain stable across a routed boundary and which can
   change.

3. Identify every component that may create independent session state.

4. State which representation is required to answer the current question.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Track frame 5 as a frame, packet, and TCP flow;
identify what session state remains hidden.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number == 3 || frame.number == 5 || frame.number == 6' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e vlan.id -e tcp.flags
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'tcp' -T fields -E header=y -e frame.number -e ip.src -e ip.dst -e tcp.flags -e tcp.seq -e tcp.ack -e http.response.code
```

## Expected Evidence and Worked Reasoning

Ethernet, IP, and TCP fields describe different scopes. Flags describe
transport progress; no firewall session table is in this capture.

## Completion Standard

Cite a field for each representation and one absent state source.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is the destination MAC address usually not the remote server's MAC
   address?

2. Can two tools report different session counts for the same traffic without
   either being wrong?

3. Which fields normally define a five-tuple flow?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)

[RFC 826 — packet generation and reception](https://www.rfc-editor.org/rfc/rfc826.html)
