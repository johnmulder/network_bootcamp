# Control, Data, and Management Planes

> **Module 1 · Section 1**

## Why It Matters

The three-plane model separates how forwarding knowledge is learned, how
packets are moved, and how operators observe or change a device. It is
essential for explaining partial failures.

## Core Model

* The control plane exchanges or calculates information used to build
  forwarding state, such as routes, neighbors, and spanning-tree decisions.

* The data plane applies installed forwarding state to packets at operational
  speed.

* The management plane exposes configuration, telemetry, authentication,
  software lifecycle, and administrative access.

* A control-plane failure may leave stale data-plane state temporarily working.
  A management-plane failure may prevent access while forwarding continues.

* Policies can affect more than one plane, so an investigation must identify
  which plane produced or enforced a decision.

## Reasoning Process

1. Name the observed symptom and determine whether forwarding, learning, or
   administration is affected.

2. Identify the relevant state in each plane: learned information, installed
   forwarding entry, and management evidence.

3. Check whether the planes agree or whether one contains stale, missing, or
   inaccessible state.

4. Predict what should persist and what should converge after a failure.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether an LSA and a forwarding-table change
happen at the same recorded instant.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/route-events.jsonl
```

## Expected Evidence and Worked Reasoning

The event log distinguishes ospf_lsa from fib_install and later flow_rehash.
No management login or application recovery observation is supplied.

## Completion Standard

Classify three events by plane and name an unobserved plane.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can the data plane continue when the control plane is unavailable?

2. Why does successful management access not prove application forwarding
   works?

3. Which plane would explain a correct route that was never installed for
   forwarding?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 2328 §§10, 16 — adjacency and route calculation](https://www.rfc-editor.org/rfc/rfc2328.html)

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
