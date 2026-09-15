# Link, VLAN, and Address-Resolution Checks

> **Module 1 · Section 7**

## Why It Matters

The earliest forwarding dependencies are physical or logical link state, VLAN
membership, and neighbor resolution. Failures here should be proven before
investigating remote routing.

## Core Model

* Link state establishes only local connectivity; it does not prove correct
  VLAN, addressing, or end-to-end service.

* VLAN mismatches can isolate a host while leaving interfaces operational.

* ARP or Neighbor Discovery failure can result from wrong prefix, missing peer,
  filtering, duplicate addresses, or stale state.

* MAC and neighbor tables have age and observation-point limitations.

* Broadcast-domain symptoms should be separated from routed-path symptoms.

## Reasoning Process

1. Verify interface state, counters, and expected local attachment from
   fixture evidence.

2. Confirm effective VLAN on access and trunk links.

3. Check address, prefix, duplicate, and gateway assumptions.

4. Trace ARP or Neighbor Discovery and correlate it with switch learning.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which of L1–L4 distinguishes link failure,
wrong VLAN, unresolved neighbor, and no listener.

Run from the repository root:

```sh
jq '.' labs/fixtures/network/troubleshooting.json
```

## Expected Evidence and Worked Reasoning

L1 is link-down; L2 is learned in VLAN 20 instead of 10; L3 lacks a neighbor
response with peer state unknown; L4 combines host socket inventory with
SYN/RST. Counters alone do not locate every fault.

## Completion Standard

Cite each decisive field and preserve L3's unresolved cause.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why does an up interface not prove correct VLAN membership?

2. What evidence separates unanswered ARP from a missing route?

3. How can a duplicate address appear intermittent?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 826 — packet generation and reception](https://www.rfc-editor.org/rfc/rfc826.html)

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
