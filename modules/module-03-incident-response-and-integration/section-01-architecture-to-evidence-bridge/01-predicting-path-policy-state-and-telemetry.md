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

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the firewall record expected for F2, then
compare the supplied decision.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

Intended deny differs from the TEMP-EGRESS-17 allow record. The discrepancy
warrants a rule-history check, not an invented compromise verdict.

## Completion Standard

Map one intended event to a source and explain the mismatch.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What should a firewall log if traffic never reaches it?

2. Why can the absence of NetFlow be compatible with a real connection?

3. Which observation would force you to revise the architecture model?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
