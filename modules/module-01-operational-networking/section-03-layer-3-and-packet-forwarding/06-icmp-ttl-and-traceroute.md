# ICMP, TTL, and Traceroute

> **Module 1 · Section 3**

## Why It Matters

ICMP reports network-layer conditions and supports diagnostics. TTL or Hop
Limit prevents persistent loops, while traceroute turns expiration messages
into a partial path view.

## Core Model

* IPv4 TTL and IPv6 Hop Limit are decremented by each router; expiration
  normally causes an ICMP time-exceeded message.

* ICMP also reports unreachable destinations, fragmentation needs, and other
  control information.

* Traceroute sends probes with increasing TTL or Hop Limit and records
  responding devices.

* Responses can be filtered, rate-limited, sourced from unexpected interfaces,
  or follow a different return path.

* A traceroute result is evidence about probe and response behavior, not a
  complete proof of the application path.

## Reasoning Process

1. Identify the traceroute probe type, destination port or identifier, and
   increasing lifetime.

2. Map each response to the probe that triggered it.

3. Account for missing, repeated, or load-balanced hops.

4. Compare traceroute with routing and application evidence before reaching a
   conclusion.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether an unanswered third traceroute probe
means the route ends there.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/traceroute.json
```

## Expected Evidence and Worked Reasoning

Hop 3 is unknown in the saved probe results. Later responses can coexist with
intermediate silence; probe handling differs from application delivery.

## Completion Standard

Cite the silent hop and give a distinguishable filtering alternative.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can a router forward application traffic but not appear in traceroute?

2. Does the source address of an ICMP reply always identify the traversed
   interface?

3. What does an asterisk in traceroute actually prove?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
