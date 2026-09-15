# Packet-Path Foundation Check

> **Module 2 · Section 1**

## Why It Matters

Architecture analysis begins with packet behavior. This foundation check
confirms that a participant can turn a diagram into forward and return paths
without inventing missing details.

## Core Model

* A line on a diagram shows an intended relationship, not necessarily Layer 2
  adjacency, Layer 3 reachability, policy permission, or current health.

* Every flow requires endpoint configuration, a forwarding path, a return path,
  applicable policy, and any state created by middleboxes.

* Architecture decisions should be evaluated against requirements and failure
  behavior rather than visual symmetry.

* Unknown routing contexts, address translation, encryption, ownership, or
  telemetry must be recorded explicitly.

* The same reference flow will be reused throughout the module to compare
  design choices.

## Reasoning Process

1. Select a source, destination, protocol, direction, and success criterion.

2. Trace Layer 2 and Layer 3 transitions using only the facts provided.

3. Mark routing, policy, state, trust, failure, and visibility boundaries.

4. List unresolved questions before evaluating whether the design is good.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict what the foundations trunk can establish
about F3 server-to-historian policy.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number == 3 || frame.number == 5 || frame.number == 6' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e vlan.id -e tcp.flags
column -s, -t labs/fixtures/architecture/traffic-flows.csv
```

## Expected Evidence and Worked Reasoning

The trunk records a workstation/application exchange, while F3 is a separate
intended server/historian flow. One cannot validate the other.

## Completion Standard

State scope and one missing enforcement observation.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which parts of your path are confirmed and which are inferred?

2. Did you independently establish the return path?

3. What missing fact would most change your architecture assessment?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
