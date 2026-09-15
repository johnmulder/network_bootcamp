# Default Gateways and Routing Tables

> **Module 1 · Section 3**

## Why It Matters

A routing table is the central data structure for choosing an IP packet's next
forwarding action. Hosts and routers use the same basic logic, though routers
usually hold more routes.

## Core Model

* A route contains a destination prefix plus an action such as a next hop,
  egress interface, reject, blackhole, or local delivery.

* A connected route represents a prefix directly reachable through an
  interface.

* A default route matches destinations not covered by a more-specific entry.

* A next hop must itself be reachable, often through a connected or recursively
  resolved route.

* Multiple routing tables can exist for separate contexts, so the correct table
  must be identified before interpreting entries.

## Reasoning Process

1. Choose the routing context used by the packet.

2. Collect every route whose prefix contains the destination.

3. Select the most-specific route, then resolve its next hop and egress
   interface.

4. Check whether source selection, scope, or policy routing changes the result.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the route used by this macOS snapshot for
10.0.20.40.

Run from the repository root:

```sh
cat labs/fixtures/routing/macos-routes.txt
```

## Expected Evidence and Worked Reasoning

The 10.0.20/24 entry targets 10.0.10.254 on en0; this snapshot lacks the
candidate CSV's server /32. The host table is separate from the capture model.

## Completion Standard

Cite the installed entry and avoid combining snapshots.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What makes a connected route different from a static next-hop route?

2. Why must the next-hop address be reachable?

3. Does a default route override a more-specific route?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
