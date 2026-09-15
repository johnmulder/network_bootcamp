# High Availability: Active/Active and Active/Passive

> **Module 2 · Section 2**

## Why It Matters

High availability is a service property created by redundant components, state,
health detection, and recovery behavior. Device count alone does not establish
availability.

## Core Model

* Active/passive designs keep one node serving while another waits to assume
  responsibility.

* Active/active designs serve traffic on multiple nodes, but may divide flows,
  partitions, or functions rather than duplicate every operation.

* Health checks must detect service failure, not only device power or interface
  state.

* Stateful services require session, NAT, identity, or application state to be
  synchronized or safely re-created.

* Split-brain, stale state, dependency failure, and shared infrastructure can
  defeat nominal redundancy.

## Reasoning Process

1. Define the service and its acceptable interruption, loss, and recovery
   behavior.

2. Map active responsibilities, shared state, and health signals.

3. Fail each component and dependency separately, including partial failures.

4. Verify that recovery restores both directions and does not create duplicate
   ownership.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a standby firewall with stale
synchronization preserves established NAT sessions.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/failures.jsonl
```

## Expected Evidence and Worked Reasoning

The enterprise-fw-a record explicitly affects established NAT sessions. It
does not say all new connections fail or that every application loses state.

## Completion Standard

Separate old sessions, new sessions, and required validation.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is active/active not automatically more available?

2. What makes a health check meaningful?

3. Which shared component can remain a single point of failure?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
