# Resolving the NetFlow and VRF Contradiction

> **Module 3 · Section 6**

## Why It Matters

The example claim—flow records show PLC VLAN traffic to an external address
while the VRF allegedly has no default route—contains an observation and a
configuration assertion that may both be true.

## Core Model

* The flow exporter location determines whether records describe original,
  routed, tunneled, proxied, or translated traffic.

* A VRF can reach a specific external prefix without a default route.

* Route leaking, policy routing, another routing table, proxying, NAT, a
  changed configuration, or mislabeled source can reconcile the statements.

* Flow records can be stale, sampled, mis-timestamped, duplicated, or
  attributed to the wrong interface.

* The absence of a current default route does not establish historical
  forwarding state.

## Reasoning Process

1. Define the exact flow fields, exporter, interfaces, observation domain, and
   time.

2. Identify the exact VRF and retrieve its relevant historical route
   information.

3. Test specific route, leak, proxy, NAT, policy-route, tunnel, and attribution
   explanations.

4. Request the smallest evidence set that distinguishes the remaining
   explanations.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether an OT default is required to
reconcile the recorded external flow.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/vrfs.json
jq '.' labs/fixtures/incident/flows.jsonl
```

## Expected Evidence and Worked Reasoning

The flow source is 10.0.10.23; OT's missing default describes a different
context. Exporter placement and historical context still need care.

## Completion Standard

Resolve the apparent contradiction without proposing an unnecessary default.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is a default route not required for every external destination?

2. Which observation could have occurred after the traffic left the VRF?

3. How would you test whether the source label is wrong?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4364 §3 — separate VRF forwarding tables](https://www.rfc-editor.org/rfc/rfc4364.html#section-3)

[RFC 7011 §2 — IPFIX observation and metering](https://www.rfc-editor.org/rfc/rfc7011.html#section-2)
