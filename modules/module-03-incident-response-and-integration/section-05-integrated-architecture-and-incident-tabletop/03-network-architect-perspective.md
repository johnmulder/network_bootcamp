# Network Architect Perspective

> **Module 3 · Section 5**

## Why It Matters

The network architect evaluates why boundaries exist, how dependencies and
failures shape risk, and whether the observed incident exposes a design
weakness.

## Core Model

* Trust and security boundaries should follow communication and consequence
  requirements.

* Failure domains include shared management, identity, control, software,
  facility, and provider dependencies.

* Redundancy must preserve policy, state, capacity, visibility, and safe
  recovery.

* Blast radius depends on route reachability, shared credentials, permitted
  conduits, and administrative control.

* An incident can reveal drift or misuse without proving the original
  architecture intent was wrong.

## Reasoning Process

1. Restate design requirements and intended communication.

2. Map trust, failure, management, visibility, and ownership boundaries.

3. Evaluate how the suspected path bypassed, crossed, or used those boundaries.

4. Recommend the smallest architecture improvement that reduces recurrence or
   blast radius.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which smallest design review follows from
intended deny versus a temporary permit.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/architecture/failures.jsonl
```

## Expected Evidence and Worked Reasoning

Review the temporary exception's owner, scope, and expiry; unrelated
shared-power and failure risks remain separate findings. Architecture intent
need not be wholly rejected.

## Completion Standard

Recommend one scope-limited improvement tied to a cited discrepancy.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which boundary failed to contain the suspected behavior?

2. Was the weakness architectural, configurational, operational, or
   evidentiary?

3. What change reduces risk without creating disproportionate complexity?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
