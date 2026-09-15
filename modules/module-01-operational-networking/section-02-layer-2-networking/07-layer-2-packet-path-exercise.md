# Layer 2 Packet-Path Exercise

> **Module 1 · Section 2**

## Why It Matters

This exercise combines address resolution, MAC learning, VLAN membership,
trunks, and Layer 3 boundaries into one defensible packet-path explanation.

## Core Model

* The same-VLAN path should identify ARP behavior, switch learning, flooding
  conditions, and the eventual unicast frames.

* The inter-VLAN path should identify both address-resolution events and the
  device performing routing.

* Every link should be labeled with the effective VLAN and whether the Ethernet
  frame is tagged.

* The output must distinguish facts visible in the PCAP from topology facts
  recorded in the architecture diagram.

* The return path must be traced rather than assumed.

## Reasoning Process

1. Inventory endpoints, addresses, prefixes, gateways, ports, VLANs, and
   capture points.

2. Trace the same-VLAN exchange frame by frame until both ARP and data
   forwarding are stable.

3. Trace the inter-VLAN exchange through the gateway and reconstruct new
   Ethernet headers.

4. Document uncertainties, alternate explanations, and the evidence that would
   resolve them.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Contrast local DNS delivery with the first routed
application hop.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number == 3 || frame.number == 5 || frame.number == 6' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e vlan.id -e tcp.flags
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'arp' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
```

## Expected Evidence and Worked Reasoning

Frames 3 and 5 have different Ethernet destinations for local and remote IPs.
Only the gateway ARP exchange is present. Downstream ARP and full switch
tables remain unknown.

## Completion Standard

Complete two header rows and distinguish observed return from a predicted hop.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can another participant reproduce your path using only the cited evidence?

2. Did you identify every point at which the Ethernet header changes?

3. Did you distinguish unknown-unicast flooding from broadcast behavior?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 826 — packet generation and reception](https://www.rfc-editor.org/rfc/rfc826.html)

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
