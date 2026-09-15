# Security Engineer Perspective

> **Module 3 · Section 5**

## Why It Matters

The security engineer evaluates permitted communication, enforcement,
preventive controls, monitoring placement, and opportunities to limit lateral
movement.

## Core Model

* Policy should express required flows with least privilege, explicit
  direction, identity, protocol, and ownership.

* Segmentation works only when all paths cross the intended enforcement point.

* Preventive controls include network policy, identity, endpoint hardening,
  application controls, and controlled administration.

* Detection coverage must align with important paths, encryption stages, and
  likely techniques.

* Containment and remediation should account for state, dependencies, business
  function, and OT safety.

## Reasoning Process

1. Compare observed or suspected traffic with the approved flow matrix.

2. Locate every preventive and detective control on the path.

3. Identify which control allowed, missed, blocked, or could not observe the
   behavior.

4. Prioritize a policy, endpoint, identity, or monitoring improvement by risk
   reduction.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a BYPASS proxy record means the
firewall denied the connection.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/firewall.jsonl
jq '.' labs/fixtures/incident/proxy.jsonl
```

## Expected Evidence and Worked Reasoning

The proxy bypass describes its own inspection behavior, while the firewall
records allow. Neither proves encrypted content benign or malicious.

## Completion Standard

Name each enforcement/visibility boundary and one targeted control review.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What specifically should prevent lateral movement at this boundary?

2. Which permitted communication is broader than the business need?

3. Where should monitoring occur relative to encryption termination?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
