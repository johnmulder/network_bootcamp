# Route Selection, Filtering, and Redistribution

> **Module 1 · Section 5**

## Why It Matters

Route selection turns multiple candidates into installed reachability.
Filtering and redistribution connect routing domains but can also create leaks,
loops, and unstable feedback.

## Core Model

* Each protocol first selects its own best path, after which the routing
  process compares eligible sources for installation.

* Import policy controls accepted routes and attributes; export policy controls
  what is advertised to a peer.

* Prefix filters should be explicit about exact and more-specific routes.

* Redistribution translates reachability between protocols but usually loses
  some native topology meaning.

* Mutual redistribution without tags, filtering, or clear ownership can feed
  routes back into their origin.

## Reasoning Process

1. List candidates by prefix, source protocol, attributes, and next-hop
   validity.

2. Apply protocol-specific selection before cross-protocol preference.

3. Apply import, export, and redistribution policy at named boundaries.

4. Test route withdrawal and feedback behavior, not only initial advertisement.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether BGP policy and cross-protocol route
preference are the same comparison.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/bgp.json
column -s, -t labs/fixtures/routing/route-candidates.csv
```

## Expected Evidence and Worked Reasoning

BGP compares its candidate attributes; the CSV compares eligible sources for
identical prefixes. No import/export filters or redistribution configuration
is supplied.

## Completion Standard

Explain both stages; make any proposed prefix filter explicitly hypothetical.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can a route be accepted but not installed?

2. What is the difference between an import filter and an export filter?

3. How can redistribution cause a routing loop without repeating an IP hop
   immediately?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4271 §9 — BGP decision process](https://www.rfc-editor.org/rfc/rfc4271.html#section-9)

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
