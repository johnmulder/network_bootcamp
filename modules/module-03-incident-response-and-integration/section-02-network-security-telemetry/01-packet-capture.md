# Packet Capture

> **Module 3 · Section 2**

## Why It Matters

A packet capture offers the most granular network evidence available at its
collection point, but it remains incomplete outside that point, time window,
direction, and encryption boundary.

## Core Model

* A capture can show frame and packet headers, protocol messages, size,
  ordering, timing, flags, retransmissions, and unencrypted payload.

* Capture location determines which addresses, encapsulations, translations,
  and directions are visible.

* Encryption hides application content while leaving selected metadata
  observable.

* Packet loss, snap length, offload, duplicate capture, clock error, and
  filtering can alter the record.

* A PCAP proves that the sensor recorded bytes; it does not by itself prove
  user intent, process identity, delivery beyond the sensor, or application
  success.

## Reasoning Process

1. Validate capture metadata, interface, filter, time range, link type, and
   completeness.

2. Identify the relevant tuple and reconstruct both directions or document the
   missing side.

3. Decode protocol behavior while accounting for retransmission, reassembly,
   and encryption.

4. Correlate with endpoint and infrastructure evidence before attributing
   activity.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which frame first establishes SMB application
use.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
```

## Expected Evidence and Worked Reasoning

Frames 15–16 show only SYN/SYN-ACK on port 445; no completed handshake or SMB
operation follows. The expected frame is absent.

## Completion Standard

Cite the transport evidence and state application outcome unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What exactly does a SYN in a PCAP prove?

2. How can capture placement change the visible NAT tuple?

3. Why might a packet appear malformed because of endpoint offload?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
