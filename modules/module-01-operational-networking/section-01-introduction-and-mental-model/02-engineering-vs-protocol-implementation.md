# Network Engineering vs. Protocol Implementation

> **Module 1 · Section 1**

## Why It Matters

A protocol specification defines messages and state machines; network
engineering decides where, why, and under what constraints those protocols are
used. Confusing the two leads to technically correct but operationally poor
designs.

## Core Model

* A protocol implementation answers how a host or device speaks Ethernet, IP,
  TCP, OSPF, or BGP.

* Network engineering answers how addressing, routing, redundancy, policy,
  capacity, and operations combine to provide a service.

* Interoperability is necessary but not sufficient. Two compliant devices can
  still fail because of topology, policy, timers, state, or return-path
  differences.

* Engineers reason about failure domains, change risk, observability,
  ownership, and recovery in addition to packet formats.

* Vendor syntax is an interface to a model; it is not the model itself.

## Reasoning Process

1. Identify the service requirement before naming a protocol or product.

2. Describe which protocol behavior contributes to the requirement.

3. List the operational constraints that the protocol alone does not solve.

4. Evaluate failure and recovery behavior, not only steady-state connectivity.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a TCP handshake alone guarantees the
large transfer will work.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/mtu-failure.pcap -Y 'tcp || icmp' -T fields -E header=y -e frame.number -e ip.len -e ip.hdr_len -e tcp.hdr_len -e tcp.len -e tcp.seq -e tcp.options.mss_val -e icmp.type -e icmp.code -e icmp.mtu
```

## Expected Evidence and Worked Reasoning

Small handshake packets fit while the large segment exceeds the reported path
limit. A functioning TCP implementation does not establish a usable full path.

## Completion Standard

Separate protocol progress from one operational dependency.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can a standards-compliant protocol deployment still be unreliable?

2. Which concerns belong to network engineering rather than packet encoding?

3. What remains true when a vendor command is replaced by another vendor's
   syntax?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)

[RFC 1191 §3 — path MTU discovery](https://www.rfc-editor.org/rfc/rfc1191.html#section-3)
