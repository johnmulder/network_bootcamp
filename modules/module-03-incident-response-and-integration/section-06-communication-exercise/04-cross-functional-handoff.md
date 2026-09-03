# Cross-Functional Handoff

> **Module 3 · Section 6**

## Why It Matters

A handoff should let the receiving owner act without reconstructing the
investigation or accepting unsupported conclusions.

## Core Model

* The handoff states the observation, affected service or asset, impact, time,
  and source.

* Interpretation and confidence are separate from confirmed facts.

* Unknowns and visibility limitations are explicit.

* The requested action is specific, owned, prioritized, and connected to a
  decision.

* Evidence references, safety constraints, validation, and response channel are
  included.

## Reasoning Process

1. Lead with the operational or security outcome requiring attention.

2. List concise facts with evidence references and normalized time.

3. State interpretation, alternatives, confidence, and unknowns.

4. Request one action with owner, urgency, risk, validation, and follow-up.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-06-communication-exercise
   touch work/module-03-incident-response-and-integration/section-06-communication-exercise/04-cross-functional-handoff.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Cross-Functional Handoff** in
   `work/module-03-incident-response-and-integration/section-06-communication-exercise/04-cross-functional-handoff.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq -c 'select(.dst == "198.51.100.77")' labs/fixtures/incident/flows.jsonl
   jq -c 'select(.dst == "198.51.100.77")' labs/fixtures/incident/firewall.jsonl
   jq '.OT' labs/fixtures/routing/vrfs.json
   jq -c '.' labs/fixtures/incident/proxy.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for
   **Cross-Functional Handoff**. Apply the numbered Reasoning Process in order.
   Tie every claim to a frame or log record and label it observed, inferred,
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
`work/module-03-incident-response-and-integration/section-06-communication-exercise/04-cross-functional-handoff.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Can the recipient identify exactly what action is requested?

2. Are observations visibly separate from inference?

3. What safety or rollback detail is needed before action?
