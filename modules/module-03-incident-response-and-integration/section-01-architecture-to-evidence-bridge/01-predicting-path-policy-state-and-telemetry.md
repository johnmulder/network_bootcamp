# Predicting Path, Policy, State, and Telemetry

> **Module 3 · Section 1**

## Why It Matters

An investigation should establish expected behavior and visibility before
interpreting alerts. That baseline prevents missing data from being mistaken
for proof that activity did not occur.

## Core Model

* Architecture predicts where a flow should travel, which policy should
  evaluate it, and what state should be created.

* Telemetry predictions depend on collection point, direction, tuple,
  encryption stage, sampling, and sensor health.

* A flow can be real but invisible to a selected source because it bypasses
  collection, uses another path, or falls outside retention.

* Observed evidence can disprove part of the expected model and reveal drift,
  misconfiguration, or an incomplete diagram.

* The bridge artifact links every expected event to a source and a stated
  visibility limitation.

## Reasoning Process

1. Select a critical flow and define its expected forward and return paths.

2. Mark every route, policy, state, translation, and encryption boundary.

3. Predict packet, flow, infrastructure, endpoint, and aggregated evidence.

4. Record visibility gaps before opening the investigation evidence.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-01-architecture-to-evidence-bridge
   touch work/module-03-incident-response-and-integration/section-01-architecture-to-evidence-bridge/01-predicting-path-policy-state-and-telemetry.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Predicting Path, Policy, State, and Telemetry** in
   `work/module-03-incident-response-and-integration/section-01-architecture-to-evidence-bridge/01-predicting-path-policy-state-and-telemetry.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq '.' labs/fixtures/routing/vrfs.json
   jq '.' labs/fixtures/incident/assets.json
   ```

4. In the output file, add a `## Evidence Analysis` section for **Predicting
   Path, Policy, State, and Telemetry**. Apply the numbered Reasoning Process in
   order. Tie every claim to a frame or log record and label it observed,
   inferred, hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `source`, `raw time`,
   `normalized time`, `entity`, `observation`, `classification`, `limitation`,
   and `confidence`. Cite exact frames or records.

6. Apply every step in the Reasoning Process, answer all Check Your
   Understanding questions, and keep at least one plausible alternative
   hypothesis in the same output file.

## Expected Evidence

* `ws-23` is `10.0.10.23` in CORP, while the OT prefixes are isolated in a
  different routing context.

* Flow `F2` is intended to be denied at the enterprise firewall and flow `F4`
  is intended to be denied at `ot-firewall-a`.

* Architecture predicts the policy points but does not prove whether packets
  arrived, rules matched, logs were retained, or endpoint activity occurred.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-01-architecture-to-evidence-bridge/01-predicting-path-policy-state-and-telemetry.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. What should a firewall log if traffic never reaches it?

2. Why can the absence of NetFlow be compatible with a real connection?

3. Which observation would force you to revise the architecture model?
