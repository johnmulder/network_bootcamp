# DHCP Address, Gateway, and DNS Assignment

> **Module 1 · Section 4**

## Why It Matters

DHCP supplies the network parameters that later routing and naming behavior
depend on. A valid lease can still contain an unusable address, gateway, or
resolver.

## Core Model

* DHCPv4 commonly follows Discover, Offer, Request, and Acknowledgment, with
  broadcast behavior during initial acquisition.

* A lease can provide address, mask or prefix, default gateway, DNS servers,
  domain information, and other options.

* Renewal normally becomes unicast when the client can reach the original
  server, then broadens during rebinding.

* Relay agents carry requests between broadcast domains and identify the client
  segment.

* Lease, relay, scope, reservation, and conflict evidence must be correlated by
  client identifier, MAC, address, and time.

## Reasoning Process

1. Identify the client, transaction identifier, requested address, and offered
   parameters.

2. Verify that the assigned address, prefix, gateway, and DNS options are
   internally consistent.

3. Determine whether a relay is present and which scope should answer.

4. Relate lease timing to the observed connectivity window.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which record establishes supplied
configuration rather than a requested lease.

Run from the repository root:

```sh
jq '.' labs/fixtures/network/dhcp.jsonl
```

## Expected Evidence and Worked Reasoning

Record 4 is ACK for transaction 0x1023 with address, prefix, gateway, and DNS.
Relay state and client installation success are not recorded.

## Completion Standard

Correlate the four messages and separate server configuration from client
health.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can DHCP succeed while the client still cannot reach its gateway?

2. What role does a relay agent play?

3. Which timestamps matter when investigating an address that changed owners?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 2131 §3 — client/server interactions](https://www.rfc-editor.org/rfc/rfc2131.html#section-3)
