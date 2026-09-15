# Link Aggregation and LACP

> **Module 1 · Section 2**

## Why It Matters

Link aggregation treats multiple physical links as one logical connection for
capacity and resilience. LACP helps both ends agree on membership, but
individual flows still follow specific members.

## Core Model

* A link aggregation group presents one logical interface while distributing
  eligible traffic across member links.

* LACP exchanges actor and partner information to detect compatible links and
  prevent some cabling or configuration errors.

* Load distribution normally uses a deterministic hash over selected frame or
  packet fields, not per-packet round robin.

* One large flow may use only one member's capacity, while many diverse flows
  can spread across members.

* A failed or inconsistent member can affect only the flows hashed to it,
  producing path-dependent symptoms.

## Reasoning Process

1. Confirm that both ends agree on the aggregation identity and active members.

2. Identify the fields used by the load-balancing hash.

3. Map observed flows to member links without assuming equal distribution.

4. Evaluate minimum-links behavior and capacity after a member failure.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether one listed flow uses both members and
whether one failed member meets minimum_links.

Run from the repository root:

```sh
jq '.lacp' labs/fixtures/network/l2-control.json
```

## Expected Evidence and Worked Reasoning

Each modeled tuple maps to one member; ae1 has two members with minimum_links
set to one. Partner state and hash algorithm are absent; capacity and
reassignment must be checked separately.

## Completion Standard

Cite a tuple/member and minimum_links; do not invent the hash.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why does adding a second link not necessarily double one transfer's
   throughput?

2. How does LACP differ from the traffic-distribution hash?

3. What symptom suggests one aggregation member is faulty?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[IEEE 802.1AX — link aggregation scope](https://1.ieee802.org/tsn/802-1ax-rev/)
