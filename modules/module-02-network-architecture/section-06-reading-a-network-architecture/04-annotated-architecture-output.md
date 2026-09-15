# Annotated Architecture Output

> **Module 2 · Section 6**

## Why It Matters

The section output combines a diagram, flow table, boundary map, and
assumptions register into an artifact other disciplines can review.

## Core Model

* The base diagram should remain readable while annotations distinguish
  different boundary types.

* The flow table provides detail that arrows cannot: tuples, routes, policy,
  state, translation, encryption, and evidence.

* Facts, assumptions, and questions must use visibly different labels.

* Failure and visibility annotations should identify coverage and gaps rather
  than promise perfect resilience or monitoring.

* The artifact should be understandable without oral explanation.

## Reasoning Process

1. Select a consistent local Markdown notation and legend.

2. Annotate components, relationships, boundaries, dependencies, and redundant
   paths.

3. Attach detailed flow rows for the most important communications.

4. Review every claim against source material and collect unresolved questions.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which diagram annotations need a separate
detailed flow row.

Run from the repository root:

```sh
cat labs/fixtures/architecture/enterprise.md
column -s, -t labs/fixtures/architecture/traffic-flows.csv
```

## Expected Evidence and Worked Reasoning

A logical zone edge cannot express source identity, port, intent, reverse
route, and collection scope alone. F3 provides tuple and policy intention but
not enforcement.

## Completion Standard

Annotate one conduit and pair it with a sourced flow row.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can a reader distinguish fact from assumption?

2. Are return paths and encryption termination visible?

3. Does the diagram remain usable after annotation?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
