# VRF Isolation Exercise

> **Module 1 · Section 6**

## Why It Matters

This exercise tests whether routing context is treated as a first-class part of
every forwarding decision.

## Core Model

* The same physical router can connect both systems while maintaining no route
  between their contexts.

* Interface membership determines the initial lookup table.

* Route leaks must be explicit and directional.

* Return reachability and policy must be evaluated separately.

* The output should identify the smallest safe change rather than proposing
  broad route sharing.

## Reasoning Process

1. Map each interface, subnet, and route to a named VRF.

2. Attempt the forward lookup using only the source context.

3. Attempt the reverse lookup using only the destination context.

4. Propose and evaluate the minimum leak and policy needed for the stated flow.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the OT lookup for a workstation destination
without importing CORP routes.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/vrfs.json
```

## Expected Evidence and Worked Reasoning

OT has no match for 10.0.10.23; other contexts cannot supply a route
automatically. Return reachability and permission are independent.

## Completion Standard

Show context, destination, result, and the smallest evidence request.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Did you accidentally use a route from the default table?

2. Does the proposed change enable both directions?

3. What unrelated destinations become reachable after the leak?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4364 §3 — separate VRF forwarding tables](https://www.rfc-editor.org/rfc/rfc4364.html#section-3)
