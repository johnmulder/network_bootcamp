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

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which question changes the decision more:
more logs, or the target operation for this login.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/endpoint.jsonl
jq '.' labs/fixtures/incident/auth.jsonl
```

## Expected Evidence and Worked Reasoning

The target authentication is recorded but its operation is absent. A
time-bounded target audit or process-to-socket record can distinguish
important hypotheses.

## Completion Standard

Name object, interval, owner, alternative answers, and action consequence.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is “Is the firewall okay?” a low-value question?

2. What should accompany a request for a routing table?

3. Which question distinguishes containment from remediation?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
