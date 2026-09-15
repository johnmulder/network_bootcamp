# Component Evaluation Framework

> **Module 2 · Section 3**

## Why It Matters

A repeatable evaluation framework prevents diagrams from becoming inventories
of boxes. Each component should be justified by behavior, dependencies, and
evidence.

## Core Model

* The primary question is what requirement or risk the component addresses.

* Routing, traffic modification, policy, state, encryption, and telemetry are
  separate capabilities.

* Every stateful or terminating component changes failure and evidence
  behavior.

* Management, identity, time, naming, update, and control-plane dependencies
  must be included.

* A component can solve one problem while creating a new choke point, blind
  spot, or shared failure.

## Reasoning Process

1. State the requirement and the component's exact role.

2. Classify its forwarding, transformation, enforcement, state, encryption, and
   telemetry behavior.

3. Trace normal and failed flows through it.

4. Record dependencies, ownership, evidence, bypass, and recovery.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which capability changes if a load balancer
terminates TLS instead of passing packets.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/components.json
```

## Expected Evidence and Worked Reasoning

The saved load-balancer model terminates TLS and maintains state. That adds
key, backend, and session dependencies; it does not describe all products.

## Completion Standard

Fill one component row from explicit capability fields plus one unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can the component route traffic without enforcing security policy?

2. Which component behaviors create separate client and server connections?

3. What evidence is lost if the component fails before logging?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
