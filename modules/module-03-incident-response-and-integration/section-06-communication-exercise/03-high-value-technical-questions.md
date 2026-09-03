# High-Value Technical Questions

> **Module 3 · Section 6**

## Why It Matters

A high-value question targets a decision point, uncertainty, or evidence gap
and can be answered with a concrete artifact.

## Core Model

* Routing questions should name the prefix, table or VRF, time, next hop, and
  return path.

* Boundary questions should ask where Layer 3, trust, policy, state,
  translation, encryption, or visibility changes.

* Telemetry questions should name source, collection point, time, coverage, and
  what the conclusion claims.

* Incident questions should separate observation, inference, lateral movement,
  scope, containment, and remediation.

* Questions that merely request more data are weaker than questions tied to
  competing explanations.

## Reasoning Process

1. State the decision that the answer will change.

2. Name the exact object, flow, time, or boundary in question.

3. Ask for the authoritative table, packet, log, configuration, or owner.

4. Explain the possible answers and their consequences.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-06-communication-exercise
   touch work/module-03-incident-response-and-integration/section-06-communication-exercise/03-high-value-technical-questions.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **High-Value Technical Questions** in
   `work/module-03-incident-response-and-integration/section-06-communication-exercise/03-high-value-technical-questions.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq -c 'select(.dst == "198.51.100.77")' labs/fixtures/incident/flows.jsonl
   jq -c 'select(.dst == "198.51.100.77")' labs/fixtures/incident/firewall.jsonl
   jq '.OT' labs/fixtures/routing/vrfs.json
   jq -c '.' labs/fixtures/incident/proxy.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for **High-Value
   Technical Questions**. Apply the numbered Reasoning Process in order. Tie
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

* Flow data shows three connections from `10.0.10.23` to `198.51.100.77:443`;
  the enterprise firewall records translation to `192.0.2.44` under temporary
  egress rule `TEMP-EGRESS-17`.

* The OT VRF has no default route, but the observed external traffic originates
  in CORP, so the two statements are not actually contradictory.

* The proxy log records a temporary bypass, providing a precise owner and
  configuration question rather than a vague request to inspect the network.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-06-communication-exercise/03-high-value-technical-questions.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Why is “Is the firewall okay?” a low-value question?

2. What should accompany a request for a routing table?

3. Which question distinguishes containment from remediation?
