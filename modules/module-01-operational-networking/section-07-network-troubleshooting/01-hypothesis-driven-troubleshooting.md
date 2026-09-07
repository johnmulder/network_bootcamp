# Hypothesis-Driven Troubleshooting

> **Module 1 · Section 7**

## Why It Matters

Effective troubleshooting turns a vague symptom into a reproducible test,
predicts evidence, and changes one variable at a time. A checklist is useful
only when driven by a model.

## Core Model

* Expected behavior must specify source, destination, protocol, direction, and
  success criteria.

* Scope distinguishes one client, subnet, path, protocol, size, or time window
  from a broad outage.

* A hypothesis predicts an observation that can falsify it.

* Changing several variables destroys the ability to attribute improvement or
  failure.

* Every action and observation should be recorded with time, location, and
  command or evidence source.

## Reasoning Process

1. Restate the symptom as a precise expected-versus-observed comparison.

2. Find the smallest reliable reproduction and known-good comparison.

3. Choose the next test by information value, not by habit.

4. Record the result, update the hypothesis, and stop when evidence explains
   the behavior.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-07-network-troubleshooting
   touch work/module-01-operational-networking/section-07-network-troubleshooting/01-hypothesis-driven-troubleshooting.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Hypothesis-Driven Troubleshooting** in
   `work/module-01-operational-networking/section-07-network-troubleshooting/01-hypothesis-driven-troubleshooting.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tcpdump -nn -r labs/fixtures/pcaps/foundations.pcap
   tcpdump -nn -r labs/fixtures/pcaps/mtu-failure.pcap
   sed -n '1,120p' labs/fixtures/routing/macos-routes.txt
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Hypothesis-Driven
   Troubleshooting**. Apply the numbered Reasoning Process in order. For each
   step, cite at least one exact command result and label the statement as an
   observation or interpretation.

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
`work/module-01-operational-networking/section-07-network-troubleshooting/01-hypothesis-driven-troubleshooting.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. How does a known-good comparison narrow scope?

2. What makes a test falsifiable?

3. Why is restarting several components a weak diagnostic step?
