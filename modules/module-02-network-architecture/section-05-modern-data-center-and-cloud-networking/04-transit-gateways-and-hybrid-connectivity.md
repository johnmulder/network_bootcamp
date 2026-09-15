# Transit Gateways and Hybrid Connectivity

> **Module 2 · Section 5**

## Why It Matters

Transit constructs connect many virtual networks and on-premises sites through
centralized route exchange and policy. Scale improves, but route propagation
and blast radius become critical.

## Core Model

* A transit gateway or hub centralizes attachments and route tables for
  multiple networks.

* Attachments can associate with one route table and propagate routes to others
  under explicit policy.

* Peering, VPN, dedicated circuits, and SD-WAN can provide hybrid underlay
  paths.

* Overlapping prefixes, asymmetric propagation, summarization, and default
  routes can produce unexpected reachability.

* Central inspection requires symmetric service insertion and careful handling
  of state and return routes.

## Reasoning Process

1. Map every attachment to its associated and propagated route tables.

2. Resolve the forward and return path one transit decision at a time.

3. Check prefix overlap, route preference, default propagation, and inspection
   insertion.

4. Model attachment, circuit, route, and centralized-service failures.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether attachment to the transit hub alone
creates internet reachability.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/cloud-routes.json
```

## Expected Evidence and Worked Reasoning

on-prem associates with rt-hybrid, which contains only 10.20.0.0/16 toward
corp-vpc. No default exists there; association and propagation are distinct.

## Completion Standard

Show forward and return table lookups and a missing policy/state check.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can two attached networks still lack mutual reachability?

2. How can centralized inspection create asymmetric routing?

3. What is the blast radius of an incorrect propagated default route?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[AWS — transit route-table association and propagation](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-route-tables.html)
