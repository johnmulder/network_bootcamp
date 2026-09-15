# Network Engineer Perspective

> **Module 3 · Section 5**

## Why It Matters

The network engineer determines whether packets can traverse the modeled
infrastructure and which forwarding, state, and failure conditions explain the
observations.

## Core Model

* Reachability requires valid endpoint configuration, VLAN or segment
  attachment, routes, next hops, and return paths.

* VRFs and overlapping contexts determine which routes are eligible.

* Firewalls, NAT, tunnels, and load balancers create state and tuple
  transformations that affect forwarding.

* ECMP, high availability, and circuit failover can create transient or
  persistent asymmetry.

* Operational evidence includes route, neighbor, interface, session,
  translation, and packet facts.

## Reasoning Process

1. Resolve source and destination context, address, route, next hop, and egress
   at each boundary.

2. Trace return routes and stateful-device ownership.

3. Compare the observed tuple with transformations and capture locations.

4. Test failure, convergence, asymmetry, and stale-state explanations.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether OT's missing default explains the
external workstation flow.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/vrfs.json
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

The source 10.0.10.23 belongs to the enterprise context in this model, while
OT's table is different. Firewall NAT records do not add an OT default.

## Completion Standard

Show the correct source-context question and a bounded route claim.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which VRF contains the relevant prefix?

2. Could the observation arise from a different return path?

3. What table or session output would most strongly test the path?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4364 §3 — separate VRF forwarding tables](https://www.rfc-editor.org/rfc/rfc4364.html#section-3)

[RFC 3022 §2 — traditional NAT terminology](https://www.rfc-editor.org/rfc/rfc3022.html#section-2)
