# Leaf/Spine Architecture and Traffic Directions

> **Module 2 · Section 5**

## Why It Matters

Leaf/spine topologies provide predictable low-hop connectivity for data-center
east-west traffic while supporting north-south access through dedicated service
or border leaves.

## Core Model

* Endpoints connect to leaf switches; every leaf connects to every spine in the
  fabric.

* Spines provide transit between leaves and normally do not connect endpoints
  directly.

* East-west traffic moves between internal workloads; north-south traffic
  enters or leaves the data center.

* Equal-cost routed paths provide capacity and resilience without extending one
  Layer 2 tree through the core.

* Service insertion, border connectivity, and dual-homed endpoints can alter
  the simple two-tier path.

## Reasoning Process

1. Identify leaf, spine, border, service, and endpoint roles.

2. Trace same-leaf, cross-leaf, and north-south flows.

3. Enumerate ECMP paths and failure effects.

4. Locate routing, policy, service insertion, and observation points.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Assume leaves L1/L2 each connect to spines S1/S2, no
leaf-to-leaf link, equal costs, and hosts A on L1 and B on L2. Predict
cross-leaf paths.

This is a conceptual exercise under the assumptions above; no device
configuration or observed takeover/fabric state is supplied.

## Expected Evidence and Worked Reasoning

Two conceptual paths exist: L1-S1-L2 and L1-S2-L2. Same-leaf traffic can stay
on its leaf under local-forwarding assumptions. The cloud tables provide no
fabric links or ECMP state.

## Completion Standard

Enumerate both paths and the effect of losing S1 without inventing deployed
topology.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why does every leaf connect to every spine?

2. Where should an endpoint normally attach?

3. How can a required firewall make a nominally short east-west path longer?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 7938 §3 — data-center topology](https://www.rfc-editor.org/rfc/rfc7938.html#section-3)
