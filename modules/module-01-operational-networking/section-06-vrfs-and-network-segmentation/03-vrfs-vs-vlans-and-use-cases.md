# VRFs vs. VLANs and Segmentation Use Cases

> **Module 1 · Section 6**

## Why It Matters

VLANs and VRFs segment different forwarding layers. They are often paired, but
neither is a substitute for policy or a complete security architecture.

## Core Model

* A VLAN separates Layer 2 forwarding and broadcast domains.

* A VRF separates Layer 3 routing tables and route visibility.

* One VRF can contain many VLAN-backed subnets, and VLAN identifiers can be
  reused in unrelated contexts.

* Segmentation use cases include tenants, management, production stages,
  partner access, overlapping acquisitions, and trust zones.

* Segmentation limits reachability; firewalls or ACLs are still needed where
  communication requires explicit policy.

## Reasoning Process

1. State whether the separation requirement concerns frames, routes, policy, or
   all three.

2. Choose VLAN, VRF, or both based on the required forwarding boundary.

3. Place controlled interconnection and telemetry points.

4. Test management access, shared services, failure behavior, and route
   leakage.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether VLAN 10 and CORP name the same kind
of boundary.

Run from the repository root:

```sh
jq '.' labs/fixtures/network/l2-control.json
jq '.' labs/fixtures/routing/vrfs.json
```

## Expected Evidence and Worked Reasoning

VLAN 10 is a Layer 2 scope; CORP's table contains multiple subnets. A VLAN tag
is not the full routing context.

## Completion Standard

Contrast one frame decision with one route decision.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can two VLANs share one VRF?

2. Does placing systems in separate VRFs automatically inspect permitted
   traffic?

3. When is a VLAN boundary insufficient for route isolation?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[IEEE 802.1Q — bridges and bridged networks](https://1.ieee802.org/maintenance/p802-1q-rev/)

[RFC 4364 §3 — separate VRF forwarding tables](https://www.rfc-editor.org/rfc/rfc4364.html#section-3)
