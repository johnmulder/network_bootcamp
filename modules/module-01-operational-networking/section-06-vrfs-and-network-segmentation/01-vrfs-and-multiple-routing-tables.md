# VRFs and Multiple Routing Tables

> **Module 1 · Section 6**

## Why It Matters

A VRF creates an independent routing context on a shared device. The same
address can therefore have different reachability and meaning depending on the
selected table.

## Core Model

* A VRF associates interfaces and routes with a separate routing and forwarding
  table.

* Routes in one VRF are not automatically visible in another or in the default
  routing table.

* Overlapping address space can be used across isolated VRFs because lookups
  occur in separate contexts.

* Management, tenant, production, or trust domains can use VRFs to limit route
  visibility.

* A device name alone is insufficient for troubleshooting; the ingress
  interface and selected VRF are required.

## Reasoning Process

1. Identify the ingress interface and its routing context.

2. Use only the routes present or deliberately imported into that context.

3. Resolve the chosen next hop within the correct context.

4. Repeat the analysis for the return direction and destination-side VRF.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether one physical router implies shared
reachability for CORP and OT.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/vrfs.json
```

## Expected Evidence and Worked Reasoning

CORP and OT have separate route sets; OT has no default or user-subnet route.
Physical co-location does not import entries.

## Completion Standard

Perform a lookup in each context and cite the deciding absence/prefix.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can the same router produce different answers for one destination?

2. How do VRFs permit overlapping addresses?

3. What evidence identifies the routing context used by a packet?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4364 §3 — separate VRF forwarding tables](https://www.rfc-editor.org/rfc/rfc4364.html#section-3)
