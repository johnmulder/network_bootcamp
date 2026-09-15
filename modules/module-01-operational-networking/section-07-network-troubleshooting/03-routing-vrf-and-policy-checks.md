# Routing, VRF, and Policy Checks

> **Module 1 · Section 7**

## Why It Matters

Once local delivery works, the investigation moves to routing context, selected
paths, and policy boundaries. Configuration presence is not the same as packet
use.

## Core Model

* The lookup must occur in the routing table selected by the ingress context.

* Longest-prefix match and next-hop resolution determine forwarding before most
  downstream policy.

* ACL and firewall rules have direction, interface or zone, protocol, state,
  and order.

* A route can exist while policy denies traffic, and a permit can exist while
  no route reaches the destination.

* Logs may record only denials, only session creation, or a different
  observation tuple after NAT.

## Reasoning Process

1. Perform the forward and reverse route lookups in the correct contexts.

2. Place each policy evaluation on a specific interface, zone, or device.

3. Match the actual tuple and state to rule order and object expansion.

4. Correlate counters or logs with the test rather than relying on static text
   alone.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the F3 intended permit proves that
both routing directions exist.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/vrfs.json
column -s, -t labs/fixtures/architecture/traffic-flows.csv
```

## Expected Evidence and Worked Reasoning

The flow matrix expresses policy intent; the independent OT route model lacks
a server-subnet return. Rule ordering and actual counters are absent.

## Completion Standard

Write separate route and policy claims with source labels.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can a visible permit rule fail to match the packet?

2. How does the wrong VRF mimic a missing route?

3. What observation would prove the packet reached a policy boundary?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4364 §3 — separate VRF forwarding tables](https://www.rfc-editor.org/rfc/rfc4364.html#section-3)

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
