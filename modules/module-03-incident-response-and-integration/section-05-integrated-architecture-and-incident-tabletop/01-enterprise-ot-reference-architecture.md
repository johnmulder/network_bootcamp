# Enterprise/OT Reference Architecture

> **Module 3 · Section 5**

## Why It Matters

The integrated tabletop applies one incident to an architecture spanning
internet edge, DMZ, enterprise, OT DMZ, supervisory, cell or area, and
controller zones.

## Core Model

* Each boundary has distinct routing, policy, trust, state, management, and
  telemetry behavior.

* The enterprise and OT environments have different availability, safety,
  lifecycle, and response constraints.

* Industrial DMZ services should mediate necessary data and administrative
  exchange.

* Protected-network access may traverse multiple firewalls and independent
  identity or jump-host controls.

* Diagram lines must be converted into explicit paths and conduits before
  incident claims are evaluated.

## Reasoning Process

1. Label every zone, conduit, gateway, firewall, service, and management entry.

2. Define permitted enterprise-to-OT and OT-to-enterprise flows.

3. Trace the suspected activity in both directions through each routing and
   policy context.

4. Map telemetry, ownership, failure, and containment authority to every
   boundary.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether an enterprise server's intended
historian conduit grants direct access to PLCs.

Run from the repository root:

```sh
cat labs/fixtures/architecture/enterprise.md
column -s, -t labs/fixtures/architecture/traffic-flows.csv
```

## Expected Evidence and Worked Reasoning

F3 concerns a historian in OT DMZ 30; the logical supervisory boundary is
separate. No PLC route, session, or process observation is supplied.

## Completion Standard

Mark one allowed intention and one unsupported downstream inference.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which direct path would violate the intended zone model?

2. Where should enterprise identity be translated into controlled OT access?

3. What safety dependency constrains containment?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
