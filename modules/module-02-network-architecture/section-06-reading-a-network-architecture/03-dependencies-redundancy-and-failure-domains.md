# Dependencies, Redundancy, and Failure Domains

> **Module 2 · Section 6**

## Why It Matters

A visible data path is only one part of service availability. Hidden control,
identity, naming, management, power, and provider dependencies shape real
failure domains.

## Core Model

* Direct dependencies lie on the packet path; indirect dependencies enable
  configuration, authentication, discovery, time, or recovery.

* Redundant data paths can share controllers, credentials, software,
  facilities, or management networks.

* A component can be available while a required dependency is degraded or
  unreachable.

* Failure domains should be defined from the service perspective, not device
  category.

* Recovery dependencies deserve the same scrutiny as steady-state dependencies.

## Reasoning Process

1. Start with the service and list every required data and control dependency.

2. Group shared infrastructure and common operational ownership.

3. Fail each group and trace effects on delivery, detection, and recovery.

4. Rank dependencies by blast radius, detectability, and restoration
   difficulty.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a service dependency failure can
occur while forwarding devices remain up.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/failures.jsonl
```

## Expected Evidence and Worked Reasoning

The DNS stale-answer record affects app.example.test independently of switch
and firewall failure records. These records are separate drills, not
simultaneous faults.

## Completion Standard

Describe one direct and one indirect dependency and its distinguishing check.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can redundant firewalls still share a failure domain?

2. Which dependency is required only during recovery?

3. How does poor clock synchronization affect failure analysis?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1034 §§4–5 — name servers and resolvers](https://www.rfc-editor.org/rfc/rfc1034.html)
