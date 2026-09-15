# MAC Learning, Broadcasts, and ARP

> **Module 1 · Section 2**

## Why It Matters

Switch learning and address resolution explain how a host reaches a local peer
or default gateway before any application traffic can flow.

## Core Model

* A switch learns a source MAC address on the ingress port and associates it
  with the frame's VLAN.

* Unknown unicast and broadcast traffic is flooded only within the relevant
  broadcast domain.

* ARP maps an IPv4 address to a local MAC address using a broadcast request and
  usually a unicast reply.

* ARP caches reduce repeated broadcasts but can become stale, incomplete, or
  maliciously altered.

* A host ARPs for the destination only when it considers that destination
  on-link; otherwise it resolves the next-hop gateway.

## Reasoning Process

1. Use the host's address and prefix to decide whether the destination is
   on-link.

2. Determine the IPv4 address whose MAC address must be resolved.

3. Trace the ARP request, reply, cache entry, and first unicast data frame.

4. Compare the expected switch learning with the observed frame directions.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the client resolves the local next
hop or the remote server with ARP.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'arp' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e arp.opcode -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number == 3 || frame.number == 5 || frame.number == 6' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e vlan.id -e tcp.flags
```

## Expected Evidence and Worked Reasoning

ARP frames 1–2 concern the local gateway. The DNS peer MAC is already used in
frame 3; its preceding resolution is absent. A missing exchange can reflect
prior cache state.

## Completion Standard

Explain the resolved IP and explicitly label unseen cache history.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why does a host ARP for its gateway when contacting a remote subnet?

2. What is the difference between an unknown unicast flood and an ARP
   broadcast?

3. How can stale ARP state create intermittent connectivity?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 826 — packet generation and reception](https://www.rfc-editor.org/rfc/rfc826.html)
