# Firewall State, NAT, and Return Path

> **Module 1 · Section 7**

## Why It Matters

Stateful behavior links both directions of a flow. Missing or inconsistent
state, translation, and return routing often explain one-way or path-dependent
failures.

## Core Model

* A stateful firewall may allow return traffic based on an established session
  while denying new initiation in the opposite direction.

* NAT mappings bind pre-translation and post-translation tuples for a limited
  lifetime.

* Asymmetric paths can bypass the device holding state or present traffic to a
  peer without synchronized state.

* State synchronization can lag, omit some attributes, or fail during a device
  transition.

* Return traffic must reach the translated address and the stateful boundary
  that can reverse the mapping.

## Reasoning Process

1. Write both directional tuples before and after translation.

2. Identify the device that creates state and its expected timeout.

3. Trace the return route to the state owner or synchronized peer.

4. Compare session, NAT, and packet evidence at the same time.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict what the external NAT log can and cannot
establish about a return packet.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

The log records an allowed translated connection; it does not provide a timed
reverse packet capture or synchronized peer session table.

## Completion Standard

Name the state owner and the missing return-path evidence.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why does successful return traffic not prove reverse initiation is
   permitted?

2. What happens when a return path bypasses the NAT device?

3. Which evidence distinguishes missing state from missing routing?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 3022 §2 — traditional NAT terminology](https://www.rfc-editor.org/rfc/rfc3022.html#section-2)

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
