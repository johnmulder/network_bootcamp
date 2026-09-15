# Mapping Traffic, Controls, and Evidence

> **Module 3 · Section 4**

## Why It Matters

Every hypothesized step should be mapped to generated traffic, expected path,
encountered controls, observable telemetry, and residual artifacts.

## Core Model

* DNS, connection establishment, authentication, command execution, discovery,
  and transfer produce different traffic patterns.

* Routing and segmentation determine which controls can see or enforce each
  step.

* Policy and state affect initiation, return traffic, retries, and failure
  evidence.

* Network, endpoint, identity, and target logs should be correlated without
  treating shared derivation as independent proof.

* Failed actions can leave valuable evidence even when no session or
  application transaction completes.

## Reasoning Process

1. Define the exact source, destination, protocol, direction, and expected
   tuple for one step.

2. Trace path, policy, state, translation, encryption, and return behavior.

3. List expected evidence at every relevant collection point.

4. Compare expected and observed artifacts and explain discrepancies.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the denied user-to-OT attempt
establishes movement into supervisory control.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

The firewall records a deny for the direct attempt; the intended matrix
distinguishes server and workstation conduits. No successful OT access is
established.

## Completion Standard

Trace the attempted boundary and state which control observation limits scope.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Where would a denied connection leave evidence?

2. Which sensor sees the pre-NAT identity?

3. How can a failed authentication still support scoping?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
