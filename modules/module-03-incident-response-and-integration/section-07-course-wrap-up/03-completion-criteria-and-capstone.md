# Completion Criteria and Capstone

> **Module 3 · Section 7**

## Why It Matters

Completion means producing a reproducible, evidence-backed cross-functional
analysis on one Mac—not memorizing every protocol or command.

## Core Model

* The participant traces representative forward and return flows and explains
  forwarding, policy, and state.

* The architecture artifact marks trust, failure, management, and visibility
  boundaries.

* The telemetry analysis states what each source proves, suggests, and cannot
  show.

* The incident narrative separates observations, inference, hypotheses, and
  unknowns.

* The final recommendation identifies the highest-value evidence or
  proportionate containment action.

## Reasoning Process

1. Complete the packet-path trace from Module 1.

2. Complete the architecture annotation and failure assessment from Module 2.

3. Complete the evidence ledger, incident narrative, and joint action plan from
   Module 3.

4. Perform a final provenance, uncertainty, safety, and reproducibility review.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-07-course-wrap-up
   touch work/module-03-incident-response-and-integration/section-07-course-wrap-up/03-completion-criteria-and-capstone.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Completion Criteria and Capstone** in
   `work/module-03-incident-response-and-integration/section-07-course-wrap-up/03-completion-criteria-and-capstone.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   python3 labs/build_fixtures.py --check
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq -c '.' labs/fixtures/incident/flows.jsonl
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   jq -c '.' labs/fixtures/incident/endpoint.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for **Completion
   Criteria and Capstone**. Apply the numbered Reasoning Process in order. Tie
   every claim to a frame or log record and label it observed, inferred,
   hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `evidence ID`, `source`,
   `collection point`, `raw time`, `normalized time`, `entity`, `observation`,
   `classification`, `limitation`, and `confidence`. Cite exact frames or
   records.

6. Apply every step in the Reasoning Process, answer all Check Your
   Understanding questions, and keep at least one plausible alternative
   hypothesis in the same output file.

## Expected Evidence

* The final model separates intended policy from observed behavior: external
  workstation TLS is intended to be denied but is allowed by a temporary
  firewall rule.

* Endpoint records associate a process with DNS; packets show repeated
  ClientHello messages; authentication records a successful network login;
  the firewall records an OT deny. Completed TLS and SMB file access remain
  unknown, and stronger attack claims remain hypotheses.

* A complete capstone cites fixture evidence, names the return-path and
  visibility assumptions, recommends removal or review of the temporary rule,
  and identifies proportionate containment.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-07-course-wrap-up/03-completion-criteria-and-capstone.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Can every major claim be reproduced from a cited local source?

2. Did the analysis independently establish the return path?

3. Is the next action owned, proportionate, testable, and reversible?
