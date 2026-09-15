# Course Objectives and Shared Language

> **Module 1 · Section 1**

## Why It Matters

Network work crosses engineering, architecture, security, and incident
response. A shared vocabulary prevents each discipline from describing the same
packet path with incompatible assumptions.

## Core Model

* Operational fluency means being able to explain a path, identify the deciding
  device or table, and state what evidence supports the explanation.

* Architecture describes intended structure and constraints; engineering
  operates that structure; security defines and enforces acceptable behavior;
  incident response reconstructs observed behavior.

* A useful explanation names endpoints, addresses, protocols, direction,
  boundaries, state, and evidence instead of saying only that a connection
  works or fails.

* Terms should be tied to observable behavior. For example, a route is an entry
  used for forwarding, while a session is state maintained by endpoints or
  middleboxes.

* The course values defensible reasoning over memorizing vendor commands.

## Reasoning Process

1. State the behavior being explained in one sentence, including source,
   destination, protocol, and direction.

2. Name the relevant layers and boundaries without assuming a device performs a
   function merely because it appears on a diagram.

3. Separate configuration facts, observed evidence, and working assumptions.

4. Translate the conclusion into language that each participating discipline
   can verify.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Explain why one application request has two different
destination addresses.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number == 3 || frame.number == 5 || frame.number == 6' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e vlan.id -e tcp.flags
```

## Expected Evidence and Worked Reasoning

Frame 5 addresses Ethernet to the gateway while IP targets 10.0.20.40. The
trunk sees one delivery step, not every hop.

## Completion Standard

Name the two address scopes and cite frame 5.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can you distinguish an architecture claim from an observation about live
   traffic?

2. What details are missing from the statement, “The firewall blocked it”?

3. How would a network engineer and an incident responder describe the same
   failed connection differently?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)

[RFC 826 — packet generation and reception](https://www.rfc-editor.org/rfc/rfc826.html)
