# Longest Prefix, Next Hop, and Default Routes

> **Module 1 · Section 3**

## Why It Matters

Separate route installation from packet forwarding. The control plane selects
paths for each prefix; the forwarding plane looks up a packet destination in
the installed table. It does not rerun routing protocols for every packet.

## Core Model

* Longest-prefix match compares prefix length among all destination matches,
  regardless of which protocol installed them.

* Administrative preference or distance helps select which source installs
  a route for the same prefix. A preferred default does not displace an
  installed, matching host route during forwarding.

* Metrics compare paths within a routing protocol and are not inherently
  comparable across protocols.

* A default route is a zero-length prefix and therefore the least-specific
  possible match.

* Recursive resolution can make the installed forwarding path depend on another
  route to the advertised next hop.

## Reasoning Process

1. Identify the routing context and whether the input is a candidate list
   or an installed forwarding table.

2. For candidates, select paths for each identical prefix using the modeled
   source preference, metric, and multipath rules. Protocols have their own
   selection procedures; this CSV is a simplified model.

3. For a packet, select the longest matching prefix in the resulting table.

4. Resolve the selected next hop and egress adjacency. An installed route
   alone does not establish neighbor resolution or successful delivery.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the server /32 or the
lower-preference default determines the lookup.

Run from the repository root:

```sh
column -s, -t labs/fixtures/routing/route-candidates.csv
```

## Expected Evidence and Worked Reasoning

10.0.20.40/32 wins with next hop 10.0.10.252. Removing it leaves two equal /24
candidates. The CSV models selection; it does not observe one flow's chosen
member.

## Completion Standard

Separate per-prefix installation from per-packet longest match.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can a `/32` route override a default route with a better metric?

2. When is administrative preference relevant?

3. What new failure can recursive next-hop resolution introduce?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
