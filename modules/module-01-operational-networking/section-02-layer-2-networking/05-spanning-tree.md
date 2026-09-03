# Spanning Tree Protocol

> **Module 1 · Section 2**

## Why It Matters

Redundant Layer 2 links can create persistent loops because Ethernet has no hop
limit. Spanning Tree selects a loop-free active topology while retaining backup
links.

## Core Model

* STP elects a root bridge using bridge identifiers and calculates lowest-cost
  paths toward it.

* Port roles and states determine which links forward frames and which remain
  blocked to prevent loops.

* RSTP accelerates convergence by using improved roles and handshakes while
  preserving the loop-free objective.

* A topology change can move MAC addresses, cause temporary flooding, and alter
  the packet path.

* An unexpected root or inconsistent protection setting can enlarge failure
  domains even when connectivity appears normal.

## Reasoning Process

1. Identify the elected root and each switch's best path toward it.

2. Assign root, designated, alternate, and edge roles where applicable.

3. Remove non-forwarding links and verify that the remaining topology is
   loop-free.

4. Fail one active link and predict the new port roles, transient flooding, and
   affected flows.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-02-layer-2-networking
   touch work/module-01-operational-networking/section-02-layer-2-networking/05-spanning-tree.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Spanning Tree Protocol** in
   `work/module-01-operational-networking/section-02-layer-2-networking/05-spanning-tree.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'arp || vlan' -T fields -E header=y -E separator=, -e frame.number -e vlan.id -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
   jq '.stp, .lacp' labs/fixtures/network/l2-control.json
   ```

4. In the output file, add a `## Analysis` section for **Spanning Tree
   Protocol**. Apply the numbered Reasoning Process in order. For each step,
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
`work/module-01-operational-networking/section-02-layer-2-networking/05-spanning-tree.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why are redundant Layer 2 links dangerous without a loop-prevention
   protocol?

2. What traffic effect can occur while switches relearn MAC locations?

3. How can the root bridge influence real traffic paths?
