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

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict what the next shift needs beyond a list of
suspicious IP addresses.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/firewall.jsonl
jq '.' labs/fixtures/incident/auth.jsonl
```

## Expected Evidence and Worked Reasoning

A translated allow and successful network authentication support a bounded
summary. They do not establish theft or execution. The recipient needs source,
time, owner, and an exact next check.

## Completion Standard

Write a handoff under 150 words and have a reader restate the next action.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can the recipient identify exactly what action is requested?

2. Are observations visibly separate from inference?

3. What safety or rollback detail is needed before action?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
