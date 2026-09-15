# Ethernet and MAC Addressing

> **Module 1 · Section 2**

## Why It Matters

Ethernet provides delivery within a Layer 2 domain. Understanding its
addressing and frame behavior is the foundation for interpreting captures and
switch forwarding.

## Core Model

* An Ethernet frame contains destination and source MAC addresses, an EtherType
  or length field, payload, and a frame check sequence on the wire.

* A unicast destination identifies one interface, a broadcast targets all
  stations in the broadcast domain, and multicast identifies a subscribed
  group.

* MAC addresses are link-layer identifiers, not proof of a device's identity,
  ownership, or physical location.

* Switches forward frames based on learned destination MAC locations; hosts do
  not normally know the complete Layer 2 topology.

* Routers remove the incoming Layer 2 header and construct a new frame for the
  next link.

## Reasoning Process

1. Identify the ingress link and the frame's source and destination MAC
   addresses.

2. Classify the destination as unicast, multicast, or broadcast.

3. Use the EtherType to identify the encapsulated protocol.

4. Predict whether a switch forwards to one port, floods within a VLAN, or
   discards the frame.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the Ethernet destination for the ARP request
and classify it.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'arp' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
```

## Expected Evidence and Worked Reasoning

Frame 1 is broadcast to ff:ff:ff:ff:ff:ff; frame 2 supplies a reply. A capture
does not reveal the switch output-port table.

## Completion Standard

Cite MAC and opcode; distinguish observed frame from predicted switch action.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which Ethernet fields change after a router forwards an IP packet?

2. Why is a MAC address not a trustworthy user identity?

3. When does a switch need to flood a unicast frame?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 826 — packet generation and reception](https://www.rfc-editor.org/rfc/rfc826.html)
