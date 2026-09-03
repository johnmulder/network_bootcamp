# Link Aggregation and LACP

> **Module 1 · Section 2**

## Why It Matters

Link aggregation treats multiple physical links as one logical connection for
capacity and resilience. LACP helps both ends agree on membership, but
individual flows still follow specific members.

## Core Model

* A link aggregation group presents one logical interface while distributing
  eligible traffic across member links.

* LACP exchanges actor and partner information to detect compatible links and
  prevent some cabling or configuration errors.

* Load distribution normally uses a deterministic hash over selected frame or
  packet fields, not per-packet round robin.

* One large flow may use only one member's capacity, while many diverse flows
  can spread across members.

* A failed or inconsistent member can affect only the flows hashed to it,
  producing path-dependent symptoms.

## Reasoning Process

1. Confirm that both ends agree on the aggregation identity and active members.

2. Identify the fields used by the load-balancing hash.

3. Map observed flows to member links without assuming equal distribution.

4. Evaluate minimum-links behavior and capacity after a member failure.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-02-layer-2-networking
   touch work/module-01-operational-networking/section-02-layer-2-networking/06-link-aggregation-and-lacp.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Link
   Aggregation and LACP** in
   `work/module-01-operational-networking/section-02-layer-2-networking/06-link-aggregation-and-lacp.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'arp || vlan' -T fields -E header=y -E separator=, -e frame.number -e vlan.id -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
   jq '.stp, .lacp' labs/fixtures/network/l2-control.json
   ```

4. In the output file, add a `## Analysis` section for **Link Aggregation and
   LACP**. Apply the numbered Reasoning Process in order. For each step, cite at
   least one exact command result and label the statement as an observation or
   interpretation.

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
`work/module-01-operational-networking/section-02-layer-2-networking/06-link-aggregation-and-lacp.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why does adding a second link not necessarily double one transfer's
   throughput?

2. How does LACP differ from the traffic-distribution hash?

3. What symptom suggests one aggregation member is faulty?
