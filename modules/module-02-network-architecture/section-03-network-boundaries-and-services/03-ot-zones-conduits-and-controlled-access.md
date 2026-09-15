# OT Zones, Conduits, and Controlled Access

> **Module 2 · Section 3**

## Why It Matters

Operational technology networks prioritize safe and reliable physical
processes. Their segmentation and access patterns must reflect consequence,
lifecycle, and protocol constraints.

## Core Model

* Zones group assets with similar function, criticality, and security
  requirements; conduits define controlled communication between zones.

* An industrial DMZ separates enterprise services from supervisory and control
  networks and hosts approved transfer functions.

* Jump hosts and controlled remote-access paths concentrate authentication,
  recording, and policy enforcement.

* PLCs, IEDs, HMIs, historians, and engineering workstations have different
  communication and availability needs.

* Safety, deterministic operation, long equipment lifecycles, and limited
  maintenance windows constrain containment and scanning.

## Reasoning Process

1. Identify the physical process and the systems that observe or control it.

2. Group assets by function and consequence rather than IP range alone.

3. Define required conduits and prohibit direct paths that bypass the
   industrial DMZ.

4. Evaluate maintenance, vendor access, monitoring, failure, and safe recovery.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which approved enterprise/OT relationship is
narrow enough to review with a process owner.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
cat labs/fixtures/architecture/enterprise.md
```

## Expected Evidence and Worked Reasoning

F3 names server 10.0.20.40 to historian 10.0.30.50 TCP/443; F4 intends to
block direct workstation access. Neither is observed PLC control traffic.

## Completion Standard

Name a conduit and owner decision without inventing a production outage.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can aggressive containment be unsafe in an OT environment?

2. What function does an industrial DMZ serve?

3. Which access should require a jump host and session recording?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
