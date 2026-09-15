# Final Mental Model

> **Module 3 · Section 7**

## Why It Matters

The final model connects intended behavior to architecture, forwarding and
policy, packet flow, telemetry, observed behavior, and reconstructed reality.

## Core Model

* Intent states what service and security behavior should occur.

* Architecture turns intent into boundaries, dependencies, paths, policy
  locations, and failure design.

* Routing, switching, and policy create the operational packet path.

* Telemetry is a selective and imperfect record of behavior, not reality
  itself.

* Incident response reconstructs the most defensible explanation and feeds
  lessons back into intent and architecture.

## Reasoning Process

1. Begin with intended behavior rather than the first alert.

2. Derive the expected path, policy, state, and evidence.

3. Compare observed evidence with the model and revise either when
   contradicted.

4. Communicate reconstructed reality with confidence, gaps, and feedback
   actions.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether observed behavior can disagree with
intent while attribution remains unresolved.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

F2 and TEMP-EGRESS-17 disagree on permission; that does not identify who
changed the rule or why. Revise the model only as far as supported.

## Completion Standard

State intent, mechanism, observation, uncertainty, and feedback action.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Where can intended and observed behavior diverge?

2. Why is telemetry not identical to packet flow?

3. How should incident lessons change architecture?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
