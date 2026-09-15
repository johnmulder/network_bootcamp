# Tabletop Assessment Output

> **Module 2 · Section 7**

## Why It Matters

A useful tabletop output is a decision record, not a transcript. It connects
affected services, observations, blast radius, recovery, and design
improvements.

## Core Model

* The output names the scenario and assumptions precisely.

* Affected flows and user-visible effects are separated from internal device
  symptoms.

* Evidence is mapped to collection points and confidence.

* Recovery steps include prerequisites, owner, risk, verification, and
  rollback.

* Design recommendations address the failure mechanism without adding
  unjustified complexity.

## Reasoning Process

1. Summarize normal design intent and the injected condition.

2. Build a state timeline from fault through recovery.

3. Record decisions, supporting evidence, and rejected alternatives.

4. Prioritize corrective actions by risk reduction, effort, and new complexity.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict what must be observed before closing the
chosen failure action.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/failures.jsonl
```

## Expected Evidence and Worked Reasoning

The records give affected objects, not post-repair acceptance. A proposed
action needs owner, rollback, and service validation; a modeled outcome is not
measured recovery.

## Completion Standard

Write a bounded action row with acceptance evidence still requested.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can the report distinguish symptom, mechanism, and root cause?

2. Does every recovery action include a verification step?

3. Would the recommendation create a new shared dependency?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
