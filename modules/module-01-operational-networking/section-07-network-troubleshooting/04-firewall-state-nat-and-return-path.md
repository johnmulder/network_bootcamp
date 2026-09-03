# Firewall State, NAT, and Return Path

> **Module 1 · Section 7**

## Why It Matters

Stateful behavior links both directions of a flow. Missing or inconsistent
state, translation, and return routing often explain one-way or path-dependent
failures.

## Core Model

* A stateful firewall may allow return traffic based on an established session
  while denying new initiation in the opposite direction.

* NAT mappings bind pre-translation and post-translation tuples for a limited
  lifetime.

* Asymmetric paths can bypass the device holding state or present traffic to a
  peer without synchronized state.

* State synchronization can lag, omit some attributes, or fail during a device
  transition.

* Return traffic must reach the translated address and the stateful boundary
  that can reverse the mapping.

## Reasoning Process

1. Write both directional tuples before and after translation.

2. Identify the device that creates state and its expected timeout.

3. Trace the return route to the state owner or synchronized peer.

4. Compare session, NAT, and packet evidence at the same time.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-07-network-troubleshooting
   touch work/module-01-operational-networking/section-07-network-troubleshooting/04-firewall-state-nat-and-return-path.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Firewall State, NAT, and Return Path** in
   `work/module-01-operational-networking/section-07-network-troubleshooting/04-firewall-state-nat-and-return-path.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tcpdump -nn -r labs/fixtures/pcaps/foundations.pcap
   tcpdump -nn -r labs/fixtures/pcaps/mtu-failure.pcap
   sed -n '1,120p' labs/fixtures/routing/macos-routes.txt
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Firewall State, NAT,
   and Return Path**. Apply the numbered Reasoning Process in order. For each
   step, cite at least one exact command result and label the statement as an
   observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The healthy baseline completes ARP, DNS, TCP, HTTP response, and orderly TCP
  close.

* The MTU case completes the handshake but fails after a 1400-byte payload and
  ICMP MTU 1200 response.

* The firewall evidence distinguishes an allowed translated egress session,
  allowed user-to-server SMB, and denied user-to-OT HTTPS.

## Completion Standard

Submit
`work/module-01-operational-networking/section-07-network-troubleshooting/04-firewall-state-nat-and-return-path.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why does successful return traffic not prove reverse initiation is
   permitted?

2. What happens when a return path bypasses the NAT device?

3. Which evidence distinguishes missing state from missing routing?
