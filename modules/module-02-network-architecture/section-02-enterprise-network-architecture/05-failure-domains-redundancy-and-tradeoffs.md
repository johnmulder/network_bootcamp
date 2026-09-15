# Failure Domains, Redundancy, and Tradeoffs

> **Module 2 · Section 2**

## Why It Matters

Architecture must balance availability, scale, operability, cost, and
complexity. Redundancy helps only when failure modes are independent and
recovery is understandable.

## Core Model

* A failure domain is the set of services or components affected by one failure
  or change.

* Redundant elements can share hidden dependencies such as power, software,
  control plane, cabling, or upstream service.

* Complexity increases configuration combinations, testing burden, operational
  skill requirements, and recovery uncertainty.

* Availability requires detection, isolation, capacity, convergence, and
  validated procedures in addition to spare components.

* Blast radius and recovery confidence can matter more than maximizing
  theoretical redundancy.

## Reasoning Process

1. Name the service and enumerate components and dependencies on its critical
   path.

2. Group dependencies that can fail together.

3. Test whether surviving components have capacity and state to carry the
   service.

4. Compare the reliability benefit with added operational and failure
   complexity.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a redundant 200 Mbps circuit can
carry 220 Mbps of declared payload demand.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/failures.jsonl
jq '.' labs/fixtures/architecture/performance.json
```

## Expected Evidence and Worked Reasoning

The independent performance model's demands total 220 Mbps before overhead. It
cannot all fit a 200 Mbps backup; removing 60 Mbps bulk leaves 160 Mbps plus
unknown overhead/load.

## Completion Standard

Show demand arithmetic and a service prioritization tradeoff.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can two redundant devices belong to the same failure domain?

2. When does redundancy increase outage risk?

3. What evidence demonstrates that failover capacity is sufficient?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 7938 §3 — data-center topology](https://www.rfc-editor.org/rfc/rfc7938.html#section-3)
