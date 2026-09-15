# OSPF Adjacencies, LSAs, and SPF

> **Module 1 · Section 5**

## Why It Matters

OSPF distributes a link-state view within an autonomous system. Each router
builds a database and runs a shortest-path calculation rather than accepting a
neighbor's complete route choice.

## Core Model

* OSPF neighbors discover one another and form adjacencies only when key
  parameters and network conditions agree.

* Link-state advertisements describe topology and prefix information and are
  flooded through an area.

* The link-state database should be consistent among routers in the same area,
  subject to convergence timing.

* SPF calculates a shortest-path tree using interface costs and derives
  candidate routes.

* Areas limit topology scope and support hierarchy, while redistribution
  introduces routes from other sources.

## Reasoning Process

1. Verify neighbor discovery and adjacency prerequisites.

2. Map each LSA to the topology or prefix information it contributes.

3. Build the local router's shortest-path tree and total cost.

4. Explain route installation, ECMP eligibility, area behavior, and failure
   convergence.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether two FULL neighbors prove a complete
shortest-path reconstruction.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/ospf.json
```

## Expected Evidence and Worked Reasoning

R1 has two FULL neighbors and two cost-20 candidates for 10.0.20.0/24. No
complete LSDB, timer configuration, or flooding trace is supplied.

## Completion Standard

Explain the equal costs and identify what prevents building a full SPF tree.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can two routers be neighbors without reaching full adjacency?

2. What information does an LSA carry compared with an installed route?

3. How does area design limit control-plane scope?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 2328 §§10, 16 — adjacency and route calculation](https://www.rfc-editor.org/rfc/rfc2328.html)
