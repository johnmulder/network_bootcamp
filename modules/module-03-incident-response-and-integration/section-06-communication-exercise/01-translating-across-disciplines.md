# Translating Across Disciplines

> **Module 3 · Section 6**

## Why It Matters

Cross-functional communication succeeds when specialized observations are
translated into shared packet, boundary, state, and evidence terms without
erasing important nuance.

## Core Model

* Network engineering language emphasizes paths, tables, interfaces, protocols,
  and state.

* Architecture language emphasizes intent, boundaries, dependencies, failure
  domains, and tradeoffs.

* Security engineering language emphasizes policy, trust, prevention,
  detection, and exposure.

* Incident response language emphasizes evidence, timeline, scope, confidence,
  and action.

* A good translation preserves the original claim, identifies inference, and
  adds the context needed for another discipline to test it.

## Reasoning Process

1. Quote or restate the original observation without interpretation.

2. Define specialized terms and identify the observation point.

3. Translate the claim into path, policy, state, and evidence.

4. State the high-value question for each other discipline.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-06-communication-exercise
   touch work/module-03-incident-response-and-integration/section-06-communication-exercise/01-translating-across-disciplines.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Translating Across Disciplines** in
   `work/module-03-incident-response-and-integration/section-06-communication-exercise/01-translating-across-disciplines.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq -c 'select(.dst == "198.51.100.77")' labs/fixtures/incident/flows.jsonl
   jq -c 'select(.dst == "198.51.100.77")' labs/fixtures/incident/firewall.jsonl
   jq '.OT' labs/fixtures/routing/vrfs.json
   jq -c '.' labs/fixtures/incident/proxy.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for **Translating
   Across Disciplines**. Apply the numbered Reasoning Process in order. Tie
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
`work/module-03-incident-response-and-integration/section-06-communication-exercise/01-translating-across-disciplines.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. What information is lost when “blocked” is translated as “unreachable”?

2. How does a failure domain differ from incident scope?

3. Which terms should remain precise rather than simplified?
