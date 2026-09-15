# Hypothesis-Driven Troubleshooting

> **Module 1 · Section 7**

## Why It Matters

Effective troubleshooting turns a vague symptom into a reproducible test,
predicts evidence, and changes one variable at a time. A checklist is useful
only when driven by a model.

## Core Model

* Expected behavior must specify source, destination, protocol, direction, and
  success criteria.

* Scope distinguishes one client, subnet, path, protocol, size, or time window
  from a broad outage.

* A hypothesis predicts an observation that can falsify it.

* Changing several variables destroys the ability to attribute improvement or
  failure.

* Every action and observation should be recorded with time, location, and
  command or evidence source.

## Reasoning Process

1. Restate the symptom as a precise expected-versus-observed comparison.

2. Find the smallest reliable reproduction and known-good comparison.

3. Choose the next test by information value, not by habit.

4. Record the result, update the hypothesis, and stop when evidence explains
   the behavior.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict a different next check for DNS timeout D1 and
HTTP failure D4.

Run from the repository root:

```sh
jq '.' labs/fixtures/network/troubleshooting.json
```

## Expected Evidence and Worked Reasoning

D1 has no response within a bounded client window; D4 has an answer and HTTP
503. Resolver-side receipt discriminates D1; application logs are more useful
for D4.

## Completion Standard

Give two checks and explain how opposite results change the diagnosis.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. How does a known-good comparison narrow scope?

2. What makes a test falsifiable?

3. Why is restarting several components a weak diagnostic step?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 2308 §2 — negative DNS responses](https://www.rfc-editor.org/rfc/rfc2308.html#section-2)

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
