# Problem Patterns and Evidence-Bundle Exercise

> **Module 1 · Section 7**

## Why It Matters

Recurring symptom patterns are useful starting points, not diagnoses. This
exercise practices generating and eliminating multiple explanations from a
fixed evidence bundle.

## Core Model

* Gateway failure suggests local link, VLAN, address, neighbor, or
  gateway-interface problems.

* One-subnet failure suggests routing, VRF, policy, summarization, or
  return-path scope.

* One-way initiation suggests directional policy, stateful behavior, asymmetric
  routing, or application listening.

* Small-success and large-failure suggests MTU, MSS, fragmentation, buffering,
  or application limits.

* Path-dependent success suggests ECMP, aggregation members, inconsistent
  devices, or differing policy.

## Reasoning Process

1. List at least three hypotheses consistent with the symptom.

2. Identify the highest-information observation in the named fixture bundle.

3. Eliminate hypotheses only when evidence contradicts their predicted
   behavior.

4. State the leading explanation, confidence, remaining unknowns, and safest
   next test.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-07-network-troubleshooting
   touch work/module-01-operational-networking/section-07-network-troubleshooting/06-problem-patterns-and-evidence-bundle.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Problem Patterns and Evidence-Bundle Exercise** in
   `work/module-01-operational-networking/section-07-network-troubleshooting/06-problem-patterns-and-evidence-bundle.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tcpdump -nn -r labs/fixtures/pcaps/foundations.pcap
   tcpdump -nn -r labs/fixtures/pcaps/mtu-failure.pcap
   sed -n '1,120p' labs/fixtures/routing/macos-routes.txt
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Problem Patterns and
   Evidence-Bundle Exercise**. Apply the numbered Reasoning Process in order.
   For each step, cite at least one exact command result and label the statement
   as an observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The healthy baseline shows ARP, DNS, a TCP handshake, and an HTTP response.
  Frames 10–11 begin connection closure, but the final server ACK is absent;
  the capture does not establish completed TCP closure.

* The MTU case completes the handshake but fails after a 1400-byte payload and
  ICMP MTU 1200 response.

* The firewall evidence distinguishes an allowed translated egress session,
  allowed user-to-server SMB, and denied user-to-OT HTTPS.

## Completion Standard

Submit
`work/module-01-operational-networking/section-07-network-troubleshooting/06-problem-patterns-and-evidence-bundle.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Did you treat the symptom pattern as a clue rather than proof?

2. Which hypothesis remains plausible because of a visibility gap?

3. What single additional artifact would most reduce uncertainty?
