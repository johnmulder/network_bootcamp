# MPLS and SD-WAN Concepts

> **Module 2 · Section 4**

## Why It Matters

MPLS and SD-WAN are broad solution families. The useful conceptual distinction
is between provided transport, overlay control, path selection, and security
responsibility.

## Core Model

* An MPLS VPN can provide provider-managed private reachability but does not
  inherently encrypt customer traffic.

* Labels guide forwarding inside the provider network while customer routes
  define VPN reachability.

* SD-WAN commonly builds overlays across one or more transports and applies
  centralized policy to path selection.

* Application-aware steering depends on classification, link measurement,
  controller state, and edge enforcement.

* Internet, broadband, cellular, and private circuits can share an overlay
  while retaining different failure and trust properties.

## Reasoning Process

1. Identify underlay transports and who operates each one.

2. Identify overlay endpoints, route distribution, policy control, and
   encryption.

3. Trace how one application selects and changes paths.

4. Evaluate controller loss, edge failure, degraded links, and provider
   isolation.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the private MPLS transport is
encrypted and which evidence tests voice steering.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/wan.json
```

## Expected Evidence and Worked Reasoning

The model explicitly marks MPLS encryption false and voice policy lowest-loss.
Only the private circuit's loss is recorded here, so comparative live steering
remains unknown.

## Completion Standard

Cite encryption and policy fields; request comparable loss and path evidence.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Does MPLS imply encryption?

2. What information must an SD-WAN edge use to steer an application?

3. Which functions remain when the central controller is unreachable?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4364 §3 — separate VRF forwarding tables](https://www.rfc-editor.org/rfc/rfc4364.html#section-3)

[RFC 4301 §4 — IPsec security associations](https://www.rfc-editor.org/rfc/rfc4301.html#section-4)
