# Final Investigation Questions

> **Module 3 · Section 7**

## Why It Matters

Eight recurring questions provide a disciplined starting point for any network
or incident problem.

## Core Model

* What should happen establishes intent and success criteria.

* How the network makes it happen establishes path, protocols, state, and
  dependencies.

* Where policy is enforced establishes control and ownership.

* What happened and how it is known establish observations and provenance.

* What remains unknown and which explanation fits establish uncertainty and
  hypotheses.

* The next action should reduce uncertainty or risk with the least disruption.

## Reasoning Process

1. Answer each question with a fact, labeled inference, or explicit unknown.

2. Attach a source and limitation to each factual answer.

3. Use conflicting answers to identify the next test.

4. Select an action only after identifying objective, risk, authority,
   validation, and rollback.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-07-course-wrap-up
   touch work/module-03-incident-response-and-integration/section-07-course-wrap-up/02-final-investigation-questions.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Final
   Investigation Questions** in
   `work/module-03-incident-response-and-integration/section-07-course-wrap-up/02-final-investigation-questions.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Final
   Investigation Questions**. Apply the numbered Reasoning Process in order. Tie
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

* Evidence proves process-correlated DNS, periodic external TLS, one successful
  SMB authentication, and a denied OT attempt; stronger attack claims remain
  hypotheses.

* A complete capstone cites fixture evidence, names the return-path and
  visibility assumptions, recommends removal or review of the temporary rule,
  and identifies proportionate containment.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-07-course-wrap-up/02-final-investigation-questions.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Which answer is based only on intended configuration?

2. What unknown most limits the conclusion?

3. Does the proposed action reduce risk, uncertainty, or both?
