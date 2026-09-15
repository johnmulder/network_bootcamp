# ECMP and Asymmetric Routing

> **Module 1 · Section 3**

## Why It Matters

Equal-cost multipath can improve capacity and resilience, but it also creates
path diversity. Forward and return traffic may encounter different devices,
state, and telemetry.

## Core Model

* ECMP installs multiple next hops for one prefix when route attributes and
  costs are eligible.

* Forwarding usually hashes flow fields so packets in one flow remain on one
  path.

* Asymmetric routing means the reverse direction follows a different device
  sequence, not necessarily that connectivity is broken.

* Stateless routers tolerate asymmetry, while stateful firewalls, NAT, and some
  monitoring designs may not.

* Captures from one path can show only one direction and create a false
  impression of missing traffic.

## Reasoning Process

1. Enumerate all eligible forward and return next hops.

2. Identify the hash fields and any middleboxes on each possible path.

3. Mark state that must be shared or synchronized across devices.

4. Compare capture coverage with the possible path set before declaring traffic
   absent.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether two equal /24 candidates establish
the return path or per-packet striping.

Run from the repository root:

```sh
column -s, -t labs/fixtures/routing/route-candidates.csv
```

## Expected Evidence and Worked Reasoning

For another address in 10.0.20.0/24, the equal modeled next hops are .254 and
.253. No flow hash or reverse table is supplied.

## Completion Standard

List the eligible set and request one flow observation in each direction.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why does ECMP not imply per-packet load balancing?

2. When is asymmetric routing harmless?

3. How can path asymmetry produce an apparent one-sided PCAP?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
