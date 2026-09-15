# Architecture Failure-Analysis Method

> **Module 2 · Section 7**

## Why It Matters

A tabletop tests design behavior before a real outage. It should reveal
dependencies, transient states, detection gaps, unsafe actions, and recovery
assumptions.

## Core Model

* A scenario states the initiating fault, scope, timing, and any concurrent
  conditions.

* Steady-state redundancy is less important than detection, convergence, state
  preservation, and operator response.

* Partial failures often produce more confusing behavior than total component
  loss.

* User-visible symptoms, telemetry, alarms, and administrative access may
  disagree.

* Recovery actions can enlarge impact if the model is wrong.

## Reasoning Process

1. Establish normal flows, ownership, state, and evidence.

2. Inject one precisely defined failure without silently adding others.

3. Trace immediate, transient, converged, and recovery states.

4. Record symptoms, evidence, decisions, risks, and unanswered questions.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the effect of one power-loss record without
silently adding a WAN outage.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/failures.jsonl
```

## Expected Evidence and Worked Reasoning

The access-sw-1 power-loss record names ws-23 affected. The separate
stale-session and WAN-loss records describe other conditions.

## Completion Standard

Build normal/fault/validation states and keep unmeasured recovery explicit.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Did the scenario distinguish hard failure from partial degradation?

2. What evidence arrives first and which can mislead?

3. Could the proposed recovery action worsen the outage?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
