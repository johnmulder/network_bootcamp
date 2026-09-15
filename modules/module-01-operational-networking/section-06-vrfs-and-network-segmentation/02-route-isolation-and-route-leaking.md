# Route Isolation and Route Leaking

> **Module 1 · Section 6**

## Why It Matters

VRF isolation is the default absence of shared reachability. Route leaking
deliberately imports selected routes between contexts and must account for
return paths and policy.

## Core Model

* Isolation exists when no route in one context leads to the other, even if
  interfaces share a physical device.

* Route leaking can use static routes, shared services, import and export
  policies, or dedicated interconnection points.

* A leaked destination route without a corresponding return route creates
  one-way reachability.

* Shared service routes can unintentionally become transit paths if scope and
  policy are not constrained.

* Filtering, naming, NAT, and firewall behavior often interact with route
  leaking.

## Reasoning Process

1. Define the exact source and destination prefixes that require communication.

2. Select the controlled boundary where routes or traffic cross contexts.

3. Provide forward and return reachability without importing unrelated
   prefixes.

4. Apply policy and test whether either side can become unintended transit.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether adding a permit alone supplies the
missing OT return route.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/vrfs.json
column -s, -t labs/fixtures/architecture/traffic-flows.csv
```

## Expected Evidence and Worked Reasoning

F3 expresses desired server-to-historian permission, but the OT table lacks
the server prefix. A proposed leak needs scope, reverse reachability, and
policy validation.

## Completion Standard

Label a narrow leak as a proposal, not an existing or approved route.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is leaking only the destination prefix often insufficient?

2. How can a shared-services VRF become a transit risk?

3. What is the difference between route visibility and policy permission?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4364 §3 — separate VRF forwarding tables](https://www.rfc-editor.org/rfc/rfc4364.html#section-3)

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
