# ACLs and Stateful Firewalls

> **Module 2 · Section 3**

## Why It Matters

ACLs and firewalls enforce traffic policy at network boundaries. Their
placement, direction, state model, and rule semantics determine what they
actually control.

## Core Model

* An ACL commonly evaluates packet fields independently and in order, with an
  explicit or implicit final action.

* A stateful firewall creates session state and can permit return traffic
  without a separate reverse initiation rule.

* Rules depend on zones, interfaces, address objects, services, identity,
  application detection, and platform behavior.

* Routing generally decides where traffic would go; policy decides whether and
  how it may cross.

* Logging configuration, rule counters, NAT order, and asymmetric paths affect
  evidence.

## Reasoning Process

1. Normalize the observed tuple before and after any translation.

2. Place the packet at a specific interface, zone, direction, and session
   state.

3. Evaluate ordered rules and object contents exactly.

4. Check return traffic, logging, timeout, failover, and bypass behavior.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the incident's temporary rule matches
the reference F2 intention.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

F2 intends deny, but firewall record 1 records allow with TEMP-EGRESS-17. Full
rules, ordering, and return state remain unavailable.

## Completion Standard

Cite intent and observed decision separately and request rule history.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can a stateful firewall permit a reply without a reverse rule?

2. What facts are missing from the claim that a port is open?

3. How can rule order change the result?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
