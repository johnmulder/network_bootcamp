# Multisite WAN and Internet Connectivity

> **Module 2 · Section 4**

## Why It Matters

A WAN connects sites across external transport with different latency,
capacity, ownership, and failure characteristics than a campus LAN.

## Core Model

* Underlay circuits provide physical or provider transport; routing determines
  usable reachability over them.

* Sites need address plans, route exchange, security boundaries, shared
  services, and failure behavior.

* Internet connectivity can be centralized, distributed, or hybrid, changing
  egress, return paths, inspection, and identity.

* Provider handoffs and service-level objectives do not remove customer-side
  routing or capacity dependencies.

* DNS, authentication, cloud services, and management traffic can make a branch
  dependent on remote sites.

## Reasoning Process

1. Identify site requirements, critical flows, latency, capacity, and external
   dependencies.

2. Map circuits, provider boundaries, routing exchanges, and internet exits.

3. Trace forward and return paths for intersite and internet traffic.

4. Fail each circuit or hub and evaluate surviving capacity, policy, and shared
   services.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the modeled branch path to HQ and to an
unrelated destination.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/wan.json
```

## Expected Evidence and Worked Reasoning

The specific 10.0.0.0/16 route uses internet-vpn-1; the default uses private-1
through HQ. Lower circuit preference alone does not override specificity.

## Completion Standard

Trace both destination choices and state the missing reverse route.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. How does internet-exit placement affect inspection and return routing?

2. What branch services fail when the WAN is down?

3. Why does a second circuit not guarantee independent transport?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
