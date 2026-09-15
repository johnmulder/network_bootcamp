# Diagram Literacy and Boundary Identification

> **Module 2 · Section 6**

## Why It Matters

Architecture diagrams compress many kinds of relationships into shapes and
lines. Effective reading starts by decoding notation and marking what the
diagram omits.

## Core Model

* A line may represent physical connection, logical adjacency, tunnel, route
  exchange, permitted flow, or dependency.

* Layer 2, Layer 3, trust, security, failure, management, and visibility
  boundaries are related but not interchangeable.

* Icons suggest functions but do not prove routing, policy, state, translation,
  or termination behavior.

* Redundancy must be evaluated end to end, including shared dependencies.

* Diagram title, scope, version, owner, and source affect how much confidence
  it deserves.

## Reasoning Process

1. Read legend, scope, date, assumptions, and abstraction level.

2. Inventory components and classify every relationship.

3. Mark each boundary type with a distinct notation.

4. Create a questions list for missing addressing, routing, policy, state,
   ownership, and evidence.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the server-to-OT line should be read
as the server acting as a router.

Run from the repository root:

```sh
cat labs/fixtures/architecture/enterprise.md
```

## Expected Evidence and Worked Reasoning

The architecture is a logical zone model, not a cable inventory. Service
dependence and packet forwarding must be drawn separately.

## Completion Standard

Annotate relationship types and leave unspecified physical links unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What does a firewall icon prove by itself?

2. Can one link cross several boundary types?

3. Which metadata determines whether a diagram is authoritative?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
