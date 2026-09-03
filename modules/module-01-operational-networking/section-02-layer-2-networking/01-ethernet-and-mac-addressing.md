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

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-02-layer-2-networking
   touch work/module-01-operational-networking/section-02-layer-2-networking/01-ethernet-and-mac-addressing.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Ethernet and MAC Addressing** in
   `work/module-01-operational-networking/section-02-layer-2-networking/01-ethernet-and-mac-addressing.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'arp || vlan' -T fields -E header=y -E separator=, -e frame.number -e vlan.id -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
   jq '.stp, .lacp' labs/fixtures/network/l2-control.json
   ```

4. In the output file, add a `## Analysis` section for **Ethernet and MAC
   Addressing**. Apply the numbered Reasoning Process in order. For each step,
   cite at least one exact command result and label the statement as an
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
`work/module-01-operational-networking/section-02-layer-2-networking/01-ethernet-and-mac-addressing.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Which Ethernet fields change after a router forwards an IP packet?

2. Why is a MAC address not a trustworthy user identity?

3. When does a switch need to flood a unicast frame?
