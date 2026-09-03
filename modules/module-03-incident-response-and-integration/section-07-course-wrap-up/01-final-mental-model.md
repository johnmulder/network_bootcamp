# Final Mental Model

> **Module 3 · Section 7**

## Why It Matters

The final model connects intended behavior to architecture, forwarding and
policy, packet flow, telemetry, observed behavior, and reconstructed reality.

## Core Model

* Intent states what service and security behavior should occur.

* Architecture turns intent into boundaries, dependencies, paths, policy
  locations, and failure design.

* Routing, switching, and policy create the operational packet path.

* Telemetry is a selective and imperfect record of behavior, not reality
  itself.

* Incident response reconstructs the most defensible explanation and feeds
  lessons back into intent and architecture.

## Reasoning Process

1. Begin with intended behavior rather than the first alert.

2. Derive the expected path, policy, state, and evidence.

3. Compare observed evidence with the model and revise either when
   contradicted.

4. Communicate reconstructed reality with confidence, gaps, and feedback
   actions.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-07-course-wrap-up
   touch work/module-03-incident-response-and-integration/section-07-course-wrap-up/01-final-mental-model.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Final
   Mental Model** in
   `work/module-03-incident-response-and-integration/section-07-course-wrap-up/01-final-mental-model.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Final Mental
   Model**. Apply the numbered Reasoning Process in order. Tie every claim to a
   frame or log record and label it observed, inferred, hypothesized, or
   unknown.

5. Add an evidence-ledger table with the columns `source`, `raw time`,
   `normalized time`, `entity`, `observation`, `classification`, `limitation`,
   and `confidence`. Cite exact frames or records.

6. Apply every step in the Reasoning Process, answer all Check Your
   Understanding questions, and keep at least one plausible alternative
   hypothesis in the same output file.

## Expected Evidence

* The final model separates intended policy from observed behavior: external
  workstation TLS is intended to be denied but is allowed by a temporary
  firewall rule.

* Evidence proves process-correlated DNS, periodic external TLS, one successful
  SMB authentication, and a denied OT attempt; stronger attack claims remain
  hypotheses.

* A complete capstone cites fixture evidence, names the return-path and
  visibility assumptions, recommends removal or review of the temporary rule,
  and identifies proportionate containment.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-07-course-wrap-up/01-final-mental-model.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Where can intended and observed behavior diverge?

2. Why is telemetry not identical to packet flow?

3. How should incident lessons change architecture?
