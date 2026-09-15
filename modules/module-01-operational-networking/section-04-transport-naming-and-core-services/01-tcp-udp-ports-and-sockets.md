# TCP, UDP, Ports, and Sockets

> **Module 1 · Section 4**

## Why It Matters

Transport protocols connect application processes across IP networks. Ports
identify service endpoints, while sockets and tuples describe communication
from an operating-system or analytical viewpoint.

## Core Model

* TCP provides an ordered byte stream with connection state, reliability, flow
  control, and congestion control.

* UDP sends independent datagrams without transport-level delivery, ordering,
  or connection guarantees.

* A port identifies a transport endpoint within a host and protocol; TCP port
  53 and UDP port 53 are distinct.

* A listening socket accepts traffic for a local address and port, while an
  established socket includes both local and remote endpoints.

* Client source ports are usually ephemeral and are essential for
  distinguishing concurrent conversations.

## Reasoning Process

1. Identify IP protocol before interpreting port numbers.

2. Determine local and remote addresses and ports from the observation point.

3. Distinguish listening state from an established or one-way exchange.

4. Map the transport tuple to the owning process only when endpoint evidence
   supports it.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether port 80 and a completed connection
guarantee HTTP success.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'tcp' -T fields -E header=y -e frame.number -e ip.src -e ip.dst -e tcp.flags -e tcp.seq -e tcp.ack -e http.response.code
```

## Expected Evidence and Worked Reasoning

Frames 5–7 show handshake flags and frames 8–9 contain an HTTP
request/response. The application evidence is stronger than the port label;
UDP has different base semantics.

## Completion Standard

Separate transport endpoint, stream, and application observation.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is a port number meaningless without a transport protocol and host?

2. What additional state does TCP maintain that UDP does not?

3. Why can multiple clients connect to the same server port simultaneously?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
