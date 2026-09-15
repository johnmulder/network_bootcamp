# Module 2 Architecture Assessment Review

> **Module 2 · Section 8**

## Why It Matters

The review demonstrates the ability to explain an architecture's design
decisions, boundaries, dependencies, and failure modes without overstating
incomplete diagrams.

## Core Model

* The assessment begins with requirements and important traffic flows.

* Layer 2, Layer 3, trust, security, failure, management, and visibility
  boundaries are explicit.

* Redundancy is tested against shared dependencies and transient behavior.

* Cloud, WAN, management, and OT relationships are included when relevant.

* Confirmed facts, assumptions, risks, and high-value questions remain
  distinct.

## Reasoning Process

1. Establish diagram scope, authority, and missing information.

2. Trace representative forward and return flows.

3. Evaluate boundaries, dependencies, policy, telemetry, and failure behavior.

4. Write a concise assessment with evidence, risks, questions, and next
   actions.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which architectural claim is weakest when
policy, route, and outage records are kept distinct.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/architecture/cloud-routes.json
jq '.' labs/fixtures/architecture/failures.jsonl
```

## Expected Evidence and Worked Reasoning

Flow intentions, transit targets, and independent failure effects answer
different questions. They cannot establish complete enforcement, shared power
diversity, or measured service recovery.

## Completion Standard

Produce one architecture finding with evidence, scope, owner, and a next test.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Did you explain why major boundaries exist?

2. Which common-mode failure defeats the apparent redundancy?

3. What question would most change your risk assessment?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
