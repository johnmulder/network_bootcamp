# Inter-VLAN Forwarding

> **Module 1 · Section 2**

## Why It Matters

Traffic between VLANs requires a Layer 3 forwarding point. The transition
clarifies which addresses change and where routing or policy can be enforced.

## Core Model

* Hosts in different IP subnets send traffic to a default gateway rather than
  directly to the remote host's MAC address.

* The Layer 3 gateway can be a router interface, switch virtual interface,
  firewall interface, or another routed function.

* The gateway removes the incoming frame, performs a route lookup, applies
  relevant policy, and builds a new outgoing frame.

* The source and destination IP addresses usually remain unchanged, while
  source and destination MAC addresses change.

* Each routed direction can follow different devices, policies, or state, so
  the return path must be evaluated independently.

## Reasoning Process

1. Determine whether the destination is local or remote from the source host's
   perspective.

2. Resolve the source-side gateway MAC and describe the first frame.

3. At the gateway, perform the route and policy decisions for the destination
   subnet.

4. Construct the destination-side frame and repeat the analysis for the return
   path.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-02-layer-2-networking
   touch work/module-01-operational-networking/section-02-layer-2-networking/04-inter-vlan-forwarding.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Inter-VLAN Forwarding** in
   `work/module-01-operational-networking/section-02-layer-2-networking/04-inter-vlan-forwarding.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'arp || vlan' -T fields -E header=y -E separator=, -e frame.number -e vlan.id -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
   jq '.stp, .lacp' labs/fixtures/network/l2-control.json
   ```

4. In the output file, add a `## Analysis` section for **Inter-VLAN
   Forwarding**. Apply the numbered Reasoning Process in order. For each step,
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
`work/module-01-operational-networking/section-02-layer-2-networking/04-inter-vlan-forwarding.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why does the source host not need the destination host's MAC address across
   VLANs?

2. Where can an ACL be applied during inter-VLAN forwarding?

3. What facts are needed to prove the return path uses the same gateway?
