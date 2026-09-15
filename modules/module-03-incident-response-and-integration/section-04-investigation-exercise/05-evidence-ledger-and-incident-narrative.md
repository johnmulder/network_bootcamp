# Evidence Ledger and Incident Narrative

> **Module 3 · Section 4**

## Why It Matters

The investigation output must let another analyst reproduce the timeline,
challenge each claim, and understand scope, confidence, gaps, and recommended
action.

## Core Model

* The ledger records evidence identifier, source, collection point, raw
  timestamp, normalized time, entity, observation, and limitation.

* The narrative separates confirmed observations from inference and hypothesis.

* Confidence is attached to individual claims rather than the case as a whole.

* Scope includes affected and explicitly searched-but-not-found assets,
  identities, data, and intervals.

* Recommendations state evidence need, containment objective, operational risk,
  owner, validation, and rollback.

## Reasoning Process

1. Normalize and reference evidence without altering originals.

2. Build the timeline from observations before writing causal prose.

3. Group claims into confirmed, supported, unresolved, and contradicted
   findings.

4. Write the smallest defensible narrative and prioritize next evidence and
   containment.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict how changing a raw timestamp would damage
reviewability.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/auth.jsonl
python3 course.py timeline
```

## Expected Evidence and Worked Reasoning

The ledger should retain original offset time and a separate UTC value. The
generated timeline is a derived view, not a replacement for source records.

## Completion Standard

Write one complete ledger row and a claim whose confidence names its basis.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can a reviewer trace every sentence to evidence or a labeled inference?

2. Does scope use a repeatable case definition?

3. Is the recommended containment proportionate and reversible?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
