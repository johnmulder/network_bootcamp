# Access, Distribution, Core, and Collapsed Core

> **Module 2 · Section 2**

## Why It Matters

Hierarchical campus design assigns distinct responsibilities to access,
distribution, and core layers. The hierarchy is a reasoning model, not a
requirement that each role use separate hardware.

## Core Model

* The access layer connects endpoints and often supplies edge security, VLAN
  membership, power, and first-line telemetry.

* The distribution layer aggregates access, provides Layer 3 boundaries,
  applies policy, and contains failures.

* The core provides resilient high-speed transport between major blocks and
  should avoid unnecessary state or complexity.

* A collapsed core combines distribution and core roles when scale or topology
  does not justify a separate tier.

* Physical devices, logical roles, and administrative ownership may not align
  one-to-one.

## Reasoning Process

1. Identify endpoint attachment, aggregation, and transit functions on the
   diagram.

2. Assign logical roles based on behavior rather than device labels.

3. Locate routing, policy, redundancy, and management responsibilities.

4. Test whether the hierarchy contains failures and supports required growth.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Assume endpoint access switches feed one pair
performing both aggregation and transit. Classify its architectural role.

This is a conceptual exercise under the assumptions above; no device
configuration or observed takeover/fabric state is supplied.

## Expected Evidence and Worked Reasoning

That pair is a conceptual collapsed distribution/core. Labels alone do not
establish physical port counts, capacity, or failure independence.

## Completion Standard

Explain the combined roles and one growth limit under the stated assumption.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can one device perform both distribution and core roles?

2. Why should a core generally avoid unnecessary service state?

3. What requirement would justify adding a distinct distribution layer?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 7938 §3 — data-center topology](https://www.rfc-editor.org/rfc/rfc7938.html#section-3)
