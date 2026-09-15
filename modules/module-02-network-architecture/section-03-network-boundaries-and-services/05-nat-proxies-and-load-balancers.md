# NAT, Proxies, and Load Balancers

> **Module 2 · Section 3**

## Why It Matters

These services can all change traffic paths or identities, but they operate
differently. Architecture diagrams must show where connections terminate and
new ones begin.

## Core Model

* NAT rewrites packet addresses or ports while generally preserving the
  end-to-end transport connection through state.

* A forward proxy acts on behalf of clients; a reverse proxy acts on behalf of
  servers.

* A load balancer selects a backend and may pass packets, terminate transport,
  or terminate application encryption.

* Proxies and full proxies create separate client-side and server-side
  connections with independent tuples and timing.

* Health checks, persistence, source-address handling, TLS termination, and
  backend routing become service dependencies.

## Reasoning Process

1. Classify the component as translation, packet distribution, transport proxy,
   or application proxy.

2. Write client-side and server-side tuples and mark every termination point.

3. Identify selection, health, persistence, policy, and encryption behavior.

4. Determine which logs can correlate both sides of the transaction.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether every component that modifies traffic
also terminates TLS.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/components.json
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

The model marks different routing, modification, state, and TLS capabilities.
The firewall records NAT without TLS termination; the reverse proxy terminates
TLS in this model.

## Completion Standard

Contrast NAT and proxy connection boundaries; keep backend tuples unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. How does a proxy differ from destination NAT?

2. Where is the original client address preserved or lost?

3. Can a healthy load balancer still send traffic to an unusable application?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 3022 §2 — traditional NAT terminology](https://www.rfc-editor.org/rfc/rfc3022.html#section-2)

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
