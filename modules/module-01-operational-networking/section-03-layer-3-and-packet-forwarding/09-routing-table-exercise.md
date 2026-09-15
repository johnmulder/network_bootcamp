# Routing-Table Exercise

> **Module 1 · Section 3**

## Why It Matters

This exercise consolidates addressing, longest-prefix match, next-hop
resolution, ECMP, MTU, NAT, and return-path reasoning into one
packet-forwarding narrative.

## Core Model

* The selected route must be justified against every competing destination
  match.

* The next hop and egress interface must be resolved rather than copied without
  explanation.

* Forward and return decisions are independent and can use different tables or
  paths.

* Packet transformation and size constraints must be placed at specific
  boundaries.

* The final conclusion must cite the named table, diagram, or capture
  supporting each step.

## Reasoning Process

1. Normalize endpoint addresses, prefixes, routing contexts, and destination
   tuple.

2. Resolve the forward path one table at a time, including recursive next hops.

3. Apply translation, policy, and MTU effects at their modeled boundaries.

4. Repeat from the destination for the return direction and identify asymmetry.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Choose routes for the server and external-77, then
remove only the server /32.

Run from the repository root:

```sh
column -s, -t labs/fixtures/routing/route-candidates.csv
```

## Expected Evidence and Worked Reasoning

Both destinations have host routes through .252; removing the server /32
leaves its /24 choices without removing the external host route. No policy
decision follows from selection alone.

## Completion Standard

Report changed and unchanged lookups with prefix citations.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Did you explain why less-specific routes lost?

2. Did you confirm reachability of every recursive next hop?

3. Did you trace the return path instead of mirroring the forward path?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
