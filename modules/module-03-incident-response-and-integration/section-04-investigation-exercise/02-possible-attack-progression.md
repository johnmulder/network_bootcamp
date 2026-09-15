# Possible Attack Progression

> **Module 3 · Section 4**

## Why It Matters

The proposed progression—from DNS and external C2 through discovery,
credentials, lateral movement, server access, and attempted protected-network
access—is a hypothesis to test, not a prescribed story.

## Core Model

* Each proposed step has prerequisites and should produce specific network,
  endpoint, identity, or control evidence.

* A later observation does not prove every earlier step occurred.

* Benign administrative, monitoring, update, or user behavior can produce
  portions of the same sequence.

* Multiple hosts or identities may participate, and one identifier can change
  through DHCP, VPN, NAT, or reassignment.

* The order should be reconstructed from normalized evidence rather than
  diagram layout.

## Reasoning Process

1. Translate each proposed step into observable predictions and alternative
   explanations.

2. Search evidence independently for those predictions.

3. Connect steps only with shared identifiers, plausible timing, and causal
   support.

4. Remove, reorder, split, or reject steps when evidence requires it.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a later svc-backup login proves how
the account was obtained.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/endpoint.jsonl
jq '.' labs/fixtures/incident/auth.jsonl
```

## Expected Evidence and Worked Reasoning

The process/DNS sequence and later authentication can be ordered, but missing
causal links cannot be filled by a plausible attack story.

## Completion Standard

Write two supported steps and one explicitly unproven connection.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which later event could occur without credential compromise?

2. How can address reassignment create a false progression?

3. What evidence would falsify the proposed C2 step?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
