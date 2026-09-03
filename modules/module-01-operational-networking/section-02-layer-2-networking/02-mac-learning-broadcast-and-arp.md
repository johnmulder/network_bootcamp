# MAC Learning, Broadcasts, and ARP

> **Module 1 · Section 2**

## Why It Matters

Switch learning and address resolution explain how a host reaches a local peer
or default gateway before any application traffic can flow.

## Core Model

* A switch learns a source MAC address on the ingress port and associates it
  with the frame's VLAN.

* Unknown unicast and broadcast traffic is flooded only within the relevant
  broadcast domain.

* ARP maps an IPv4 address to a local MAC address using a broadcast request and
  usually a unicast reply.

* ARP caches reduce repeated broadcasts but can become stale, incomplete, or
  maliciously altered.

* A host ARPs for the destination only when it considers that destination
  on-link; otherwise it resolves the next-hop gateway.

## Reasoning Process

1. Use the host's address and prefix to decide whether the destination is
   on-link.

2. Determine the IPv4 address whose MAC address must be resolved.

3. Trace the ARP request, reply, cache entry, and first unicast data frame.

4. Compare the expected switch learning with the observed frame directions.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-02-layer-2-networking
   touch work/module-01-operational-networking/section-02-layer-2-networking/02-mac-learning-broadcast-and-arp.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **MAC
   Learning, Broadcasts, and ARP** in
   `work/module-01-operational-networking/section-02-layer-2-networking/02-mac-learning-broadcast-and-arp.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'arp || vlan' -T fields -E header=y -E separator=, -e frame.number -e vlan.id -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
   jq '.stp, .lacp' labs/fixtures/network/l2-control.json
   ```

4. In the output file, add a `## Analysis` section for **MAC Learning,
   Broadcasts, and ARP**. Apply the numbered Reasoning Process in order. For
   each step, cite at least one exact command result and label the statement as
   an observation or interpretation.

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
`work/module-01-operational-networking/section-02-layer-2-networking/02-mac-learning-broadcast-and-arp.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why does a host ARP for its gateway when contacting a remote subnet?

2. What is the difference between an unknown unicast flood and an ARP
   broadcast?

3. How can stale ARP state create intermittent connectivity?
