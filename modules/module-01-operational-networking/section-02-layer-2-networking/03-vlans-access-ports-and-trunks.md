# VLANs, Access Ports, and 802.1Q Trunks

> **Module 1 · Section 2**

## Why It Matters

VLANs create separate Layer 2 forwarding and broadcast domains on shared
switching infrastructure. Port mode determines how VLAN membership is
represented on each link.

## Core Model

* An access port carries traffic for one assigned VLAN and usually sends and
  receives untagged frames toward an endpoint.

* An 802.1Q trunk carries multiple VLANs by inserting a VLAN tag between
  Ethernet addressing and payload fields.

* The VLAN identifier is locally significant to the bridged network; it is not
  an end-to-end IP property.

* Native or untagged VLAN behavior must agree at both ends of a trunk or
  traffic can enter the wrong broadcast domain.

* Allowed-VLAN lists, port mode, and VLAN existence all influence whether a
  frame can cross a switch link.

## Reasoning Process

1. Assign every endpoint-facing link and switch-to-switch link a port mode.

2. For each frame, identify the effective VLAN at ingress, across trunks, and
   at egress.

3. Check allowed and native VLAN assumptions at both ends of every trunk.

4. Keep VLAN membership separate from IP subnetting even when the design maps
   one VLAN to one subnet.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a VLAN tag proves every link to the
server is a trunk.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number <= 5' -T fields -E header=y -e frame.number -e eth.type -e vlan.id -e eth.src -e eth.dst
```

## Expected Evidence and Worked Reasoning

The saved trunk frames carry VLAN 10. They do not disclose downstream native
or allowed-VLAN settings, endpoint-port modes, or the whole VLAN path.

## Completion Standard

Cite the tag and list two configuration facts still unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can two identical untagged frames belong to different VLANs on different
   access ports?

2. What failure results from a native VLAN mismatch?

3. Does an IP packet retain its VLAN tag across a router?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[IEEE 802.1Q — bridges and bridged networks](https://1.ieee802.org/maintenance/p802-1q-rev/)
