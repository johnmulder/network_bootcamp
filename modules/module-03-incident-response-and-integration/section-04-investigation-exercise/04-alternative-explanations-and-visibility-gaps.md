# Alternative Explanations and Visibility Gaps

> **Module 3 · Section 4**

## Why It Matters

Strong investigations actively search for benign, accidental, and different
malicious explanations. Visibility gaps determine what cannot be concluded.

## Core Model

* Common alternatives include software updates, monitoring, backup, remote
  support, administrator behavior, misconfiguration, and compromised shared
  infrastructure.

* An alternative is useful when it predicts distinguishable evidence, not when
  it is merely possible.

* Visibility gaps can result from path, encryption, retention, sensor health,
  logging policy, unsupported protocols, or missing endpoint coverage.

* Correlated absence across healthy independent sources is stronger than
  absence from one uncertain source.

* Uncertainty should guide collection and action rather than be hidden by
  confident language.

## Reasoning Process

1. For every major claim, write at least one plausible alternative.

2. Identify evidence each explanation predicts differently.

3. Evaluate whether current sources had the ability and health to record it.

4. Select the additional artifact with the highest decision value and lowest
   collection risk.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict what approved updater or target audit
evidence would do to the leading hypothesis.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/endpoint.jsonl
jq '.' labs/fixtures/incident/flows.jsonl
```

## Expected Evidence and Worked Reasoning

The supplied records are compatible with multiple causes; approval history and
target operations are missing. A useful alternative predicts a different
future observation.

## Completion Standard

Write competing predictions and request the smallest discriminating artifact.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What makes an alternative hypothesis testable?

2. When does a visibility gap prevent a negative conclusion?

3. Which missing source has the highest decision value?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
