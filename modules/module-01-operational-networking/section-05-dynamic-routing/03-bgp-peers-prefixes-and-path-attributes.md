# BGP Peers, Prefixes, and Path Attributes

> **Module 1 · Section 5**

## Why It Matters

BGP exchanges reachable prefixes and policy-bearing path attributes between
peers. It is a path-vector protocol designed for administrative control and
scale.

## Core Model

* An autonomous system is a routing domain with a common external policy,
  identified by an AS number.

* eBGP exchanges routes between autonomous systems; iBGP distributes external
  and other BGP routes within one system.

* `AS_PATH` records traversed systems and supports loop prevention and policy.

* `NEXT_HOP` identifies the address used to reach the advertised prefix and may
  require independent resolution.

* `LOCAL_PREF`, communities, filtering, and other attributes express local or
  coordinated policy.

## Reasoning Process

1. Identify the peer type, session endpoints, address family, and advertised
   prefix.

2. Read the path attributes without assuming the shortest AS path always wins.

3. Resolve the BGP next hop using the underlying routing table.

4. Apply import and export policy in the correct administrative direction.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the shortest AS path necessarily wins
this local policy.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/bgp.json
```

## Expected Evidence and Worked Reasoning

The modeled peer 192.0.2.2 has LOCAL_PREF 200 and is selected ahead of AS-path
length. Next-hop reachability still needs an independent route lookup.

## Completion Standard

Cite the competing attributes and distinguish policy from reachability.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is an established BGP session not proof that a desired prefix is
   accepted?

2. What role does `AS_PATH` play in loop prevention?

3. Why can an unresolved `NEXT_HOP` invalidate an otherwise preferred route?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 4271 §9 — BGP decision process](https://www.rfc-editor.org/rfc/rfc4271.html#section-9)
