# TCP Lifecycle and State

> **Module 1 · Section 4**

## Why It Matters

TCP's handshake, sequence space, acknowledgments, teardown, and resets reveal
whether a failure occurs before, during, or after connection establishment.

## Core Model

* The three-way handshake synchronizes initial sequence numbers and confirms
  bidirectional reachability.

* Sequence and acknowledgment numbers track bytes, not packets.

* Retransmissions can reflect loss, delay, reordering, capture gaps, or
  receiver behavior; context is required.

* FIN performs an orderly half-close, while RST immediately rejects or aborts a
  connection.

* Endpoints and stateful middleboxes can disagree about connection state
  because they observe different events or timeouts.

## Reasoning Process

1. Find SYN, SYN-ACK, and final ACK or identify the missing handshake step.

2. Follow sequence and acknowledgment progress through data transfer.

3. Interpret retransmissions alongside timing, window, and capture placement.

4. Determine which endpoint or middlebox sent FIN or RST and what preceded it.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the capture establishes complete TCP
closure in both directions.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'tcp' -T fields -E header=y -e frame.number -e ip.src -e ip.dst -e tcp.flags -e tcp.seq -e tcp.ack -e http.response.code
```

## Expected Evidence and Worked Reasoning

The trace contains SYN, SYN-ACK, ACK, data, and the start of closure; it does
not contain every final-close packet. A partial trace cannot establish final
endpoint state.

## Completion Standard

Cite opening/data/closing frames and name the missing closure evidence.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What does a SYN retransmission establish and what does it not establish?

2. How can a firewall time out state while endpoints still believe a connection
   exists?

3. Why is a reset more informative when its sender and preceding packets are
   known?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
