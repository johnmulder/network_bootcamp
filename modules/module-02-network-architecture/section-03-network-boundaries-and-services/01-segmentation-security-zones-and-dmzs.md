# Segmentation, Security Zones, and DMZs

> **Module 2 · Section 3**

## Why It Matters

Segmentation limits reachability and blast radius by placing explicit
boundaries between systems with different trust, exposure, ownership, or
operational requirements.

## Core Model

* A segment is a forwarding scope; a security zone groups systems for policy
  based on trust or function.

* A DMZ hosts services that must interact across trust boundaries without
  placing them directly inside a protected network.

* Segmentation can use VLANs, VRFs, routed links, firewalls, host controls, or
  combinations of them.

* Zone names do not enforce policy; traffic must traverse a known control point
  with explicit rules.

* Shared services and management paths can bypass intended segmentation if they
  are not modeled.

## Reasoning Process

1. Group assets by communication need, trust, exposure, ownership, and
   consequence.

2. Define allowed flows before selecting the technical boundary.

3. Place enforcement so all relevant paths, including return and management
   paths, cross it.

4. Test bypass, failure, shared-service, and recovery behavior.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a zone label itself enforces F4's
deny.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
```

## Expected Evidence and Worked Reasoning

F4 names ot-firewall-a as the intended deny point. No ordered rules or test
result is in the matrix.

## Completion Standard

Separate zone, intended conduit, and enforcement evidence.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What distinguishes a security zone from a VLAN?

2. Why is a DMZ not automatically trusted?

3. How can a shared service weaken segmentation?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
