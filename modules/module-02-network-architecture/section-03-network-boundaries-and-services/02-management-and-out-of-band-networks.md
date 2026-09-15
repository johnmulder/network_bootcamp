# Management and Out-of-Band Networks

> **Module 2 · Section 3**

## Why It Matters

Management access can change the network and therefore needs stronger
separation, identity, resilience, and monitoring than ordinary user traffic.

## Core Model

* An in-band management path shares production forwarding, while out-of-band
  management uses a separate path or interface.

* Out-of-band access can support recovery during production failures but can
  also become a high-impact attack path.

* Management networks require controlled entry, strong authentication, least
  privilege, logging, and protected name and time services.

* Console servers, jump hosts, automation systems, monitoring platforms, and
  administrators are all part of the management architecture.

* Emergency access must be tested without turning permanent bypass into normal
  practice.

## Reasoning Process

1. Inventory every way a device can be administered.

2. Trace identity, transport, and authorization from administrator to device.

3. Separate routine, automated, emergency, and vendor access paths.

4. Evaluate operation during loss of production routing, DNS, authentication,
   or the management network itself.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether MGMT and a jump-host policy establish
an independent out-of-band path.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/routing/vrfs.json
```

## Expected Evidence and Worked Reasoning

F5 intends management SSH via jump-host-policy; MGMT has its own routes.
Power, console cabling, identity availability, and actual traversal are
unspecified.

## Completion Standard

List what survives only under explicit independence assumptions.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is an out-of-band network still a security risk?

2. What services must management access survive without?

3. Where should administrative actions be logged?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
