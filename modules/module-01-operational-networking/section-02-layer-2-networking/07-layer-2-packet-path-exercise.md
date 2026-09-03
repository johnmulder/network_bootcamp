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

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-02-layer-2-networking
   touch work/module-01-operational-networking/section-02-layer-2-networking/07-layer-2-packet-path-exercise.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Layer
   2 Packet-Path Exercise** in
   `work/module-01-operational-networking/section-02-layer-2-networking/07-layer-2-packet-path-exercise.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'arp || vlan' -T fields -E header=y -E separator=, -e frame.number -e vlan.id -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
   jq '.stp, .lacp' labs/fixtures/network/l2-control.json
   ```

4. In the output file, add a `## Analysis` section for **Layer 2 Packet-Path
   Exercise**. Apply the numbered Reasoning Process in order. For each step,
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
`work/module-01-operational-networking/section-02-layer-2-networking/07-layer-2-packet-path-exercise.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Can another participant reproduce your path using only the cited evidence?

2. Did you identify every point at which the Ethernet header changes?

3. Did you distinguish unknown-unicast flooding from broadcast behavior?
