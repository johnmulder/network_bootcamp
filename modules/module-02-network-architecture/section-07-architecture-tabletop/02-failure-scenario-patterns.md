# Failure-Scenario Patterns

> **Module 2 · Section 7**

## Why It Matters

Common failure patterns help organize a tabletop while preserving the
requirement to reason from architecture-specific evidence.

## Core Model

* Access failure isolates attached endpoints; distribution or core failure can
  affect broader routing, policy, or shared services.

* Firewall failure can lose sessions, NAT mappings, inspection, or symmetric
  paths even when a peer takes over.

* WAN failure can reveal hidden site dependencies, insufficient capacity, or
  ineffective health detection.

* Routing failure can create withdrawal, leak, blackhole, loop, asymmetry, or
  slow convergence.

* Shared-service, cloud-transit, and state-synchronization failures cross
  visible device boundaries.

## Reasoning Process

1. For each pattern, identify affected flows and the smallest expected blast
   radius.

2. Predict packet, route, session, and telemetry changes.

3. Compare full failure with one plausible partial failure.

4. Choose the safest discriminating test and recovery action.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict a different validation for stale session sync
and 20-percent WAN loss.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/failures.jsonl
```

## Expected Evidence and Worked Reasoning

The former concerns established NAT sessions; the latter concerns branch
applications. A ping or device-up check cannot establish either complete
service result.

## Completion Standard

Choose a state check and a comparable performance test.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which failure produces successful small transfers but failing large ones?

2. How can incorrect route advertisement outlive the original device fault?

3. Why can firewall state synchronization failure affect only established
   flows?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
