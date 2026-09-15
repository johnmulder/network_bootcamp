# Redundant Circuits, Routing, and Failover

> **Module 2 · Section 4**

## Why It Matters

WAN resilience depends on independent transport, usable route policy,
detection, capacity, and stateful-service continuity.

## Core Model

* Circuits from different providers may still share conduit, building entry,
  exchange, or upstream infrastructure.

* Route preference decides primary and backup use; ECMP or policy can use
  multiple circuits simultaneously.

* Failure detection must distinguish hard loss from high latency, loss, or
  partial reachability.

* Backup capacity must support critical traffic and preserve required security
  inspection.

* Failback can cause a second disruption, route oscillation, or state loss if
  not controlled.

## Reasoning Process

1. Map physical and provider diversity rather than counting circuits.

2. Document normal route preference and traffic distribution.

3. Model hard, soft, partial, and upstream failures.

4. Verify detection, convergence, capacity, policy symmetry, and failback.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether an up backup is sufficient during
partial loss on the preferred circuit.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/wan.json
jq '.' labs/fixtures/architecture/performance.json
```

## Expected Evidence and Worked Reasoning

private-1 has 20 percent loss despite its lower preference number. The
separate performance comparisons show capacity differs from achieved goodput.

## Completion Standard

Explain detection, route choice, and capacity as independent requirements.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What hidden dependency can make two providers fail together?

2. Why is interface-up status an incomplete WAN health check?

3. What should be validated before automatic failback?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
