# Timelines, Scope, Hypotheses, and Containment

> **Module 3 · Section 3**

## Why It Matters

A defensible investigation maintains a normalized timeline, explicit case
definition, competing explanations, calibrated confidence, and proportionate
action.

## Core Model

* A normalized timeline preserves original timestamps and records conversion,
  precision, and clock uncertainty.

* A case definition states which observations qualify an asset, identity, or
  event as in scope.

* A hypothesis must predict evidence and remain falsifiable.

* Confidence reflects evidence quality and alternatives, not analyst
  conviction.

* Containment reduces risk but can destroy evidence, interrupt operations,
  expose the investigation, or create safety consequences.

## Reasoning Process

1. Normalize source time while preserving raw values and provenance.

2. Define scope criteria, then search consistently for matching and
   near-matching entities.

3. Maintain at least one plausible alternative hypothesis and test predictions.

4. Choose containment using threat, impact, confidence, reversibility, evidence
   preservation, and owner approval.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict UTC for 10:04:01 at offset -06:00 and whether
one-second ordering proves causation.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/auth.jsonl
python3 course.py timeline
```

## Expected Evidence and Worked Reasoning

The instant is 16:04:01Z. Raw time must remain preserved; clock accuracy and
missing socket evidence limit causal conclusions.

## Completion Standard

Convert the instant, retain provenance, and connect an action to a bounded
claim.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why should original timestamps be preserved?

2. What makes a scope definition reproducible?

3. When is delayed containment more defensible than immediate isolation?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
