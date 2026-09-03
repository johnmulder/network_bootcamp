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

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-02-layer-2-networking
   touch work/module-01-operational-networking/section-02-layer-2-networking/03-vlans-access-ports-and-trunks.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **VLANs, Access Ports, and 802.1Q Trunks** in
   `work/module-01-operational-networking/section-02-layer-2-networking/03-vlans-access-ports-and-trunks.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'arp || vlan' -T fields -E header=y -E separator=, -e frame.number -e vlan.id -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
   jq '.stp, .lacp' labs/fixtures/network/l2-control.json
   ```

4. In the output file, add a `## Analysis` section for **VLANs, Access Ports,
   and 802.1Q Trunks**. Apply the numbered Reasoning Process in order. For each
   step, cite at least one exact command result and label the statement as an
   observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* Every frame in `foundations.pcap` is tagged with VLAN 10 at the modeled trunk
  capture point.

* Frame 1 is a broadcast ARP request from `02:00:00:00:10:23` asking for
  `10.0.10.1`; frame 2 is the unicast reply from `02:00:00:00:10:01`.

* The STP root is `sw-dist-1`; the access-to-access link discards on
  `sw-access-2`; LACP flow assignments show that one flow uses one member.

## Completion Standard

Submit
`work/module-01-operational-networking/section-02-layer-2-networking/03-vlans-access-ports-and-trunks.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can two identical untagged frames belong to different VLANs on different
   access ports?

2. What failure results from a native VLAN mismatch?

3. Does an IP packet retain its VLAN tag across a router?
