# Site-to-Site IPsec and Remote-Access VPNs

> **Module 2 · Section 4**

## Why It Matters

VPNs add encrypted overlays across untrusted transport. They create new
interfaces, routes, identities, policy stages, MTU constraints, and observation
points.

## Core Model

* IPsec commonly uses IKE to authenticate peers and negotiate security
  associations for protected traffic.

* Selectors or route-based interfaces determine which traffic enters a
  site-to-site tunnel.

* Remote-access VPNs authenticate users or devices and assign addresses,
  routes, DNS, and policy.

* Split tunneling sends selected traffic outside the tunnel, while full
  tunneling directs it through the VPN.

* Encapsulation adds overhead, changes MTU, and limits what intermediate
  sensors can observe.

## Reasoning Process

1. Separate the public underlay path from the protected overlay path.

2. Identify peer or user authentication, selectors, assigned routes, and
   policy.

3. Calculate where encryption begins and ends and which tuple each sensor sees.

4. Test tunnel loss, rekey, overlapping addresses, return routing, and MTU.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether an up encrypted circuit proves a
user's VPN authentication and route assignment.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/wan.json
jq '.' labs/fixtures/incident/vpn.jsonl
```

## Expected Evidence and Worked Reasoning

The WAN model marks internet-vpn-1 encrypted; the independent incident VPN
record describes another remote session. Neither supplies a complete IPsec SA
or selector configuration.

## Completion Standard

Separate underlay, protected traffic, and user-session evidence.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can the tunnel be up while application traffic fails?

2. Why does split tunneling change security visibility?

3. Which MTU problem can encapsulation introduce?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4301 §4 — IPsec security associations](https://www.rfc-editor.org/rfc/rfc4301.html#section-4)
