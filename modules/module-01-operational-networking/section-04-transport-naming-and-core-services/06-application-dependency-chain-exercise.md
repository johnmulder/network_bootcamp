# Application Dependency-Chain Exercise

> **Module 1 · Section 4**

## Why It Matters

An application request depends on local configuration, naming, routing,
transport, encryption, and application behavior. A dependency chain makes
hidden prerequisites and failure points explicit.

## Core Model

* The chain begins before the first application packet with local
  configuration, resolver state, routes, and potentially cached information.

* Each dependency produces different traffic and evidence, and some successful
  stages can be reused from cache.

* A visible application error may originate in a lower layer or in a separate
  shared service.

* Timeouts, reattempts, and fallback behavior can create multiple flows for one
  user action.

* The output must preserve ordering and distinguish required from optional
  dependencies.

## Reasoning Process

1. Start with the user action and list every prerequisite in execution order.

2. For each step, record traffic, created state, possible failure, and
   available evidence.

3. Mark cached, retried, fallback, or parallel behavior.

4. Use timestamps and tuples to connect the stages into one narrative.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which dependencies can be reused from cache
on a second request.

Run from the repository root:

```sh
jq '.' labs/fixtures/network/dhcp.jsonl
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'dns' -T fields -E header=y -e frame.number -e ip.src -e ip.dst -e dns.qry.name -e dns.qry.type -e dns.flags.response -e dns.flags.rcode -e dns.a -e dns.resp.ttl
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'tcp' -T fields -E header=y -e frame.number -e ip.src -e ip.dst -e tcp.flags -e tcp.seq -e tcp.ack -e http.response.code
```

## Expected Evidence and Worked Reasoning

The saved lease, DNS answer, TCP handshake, and HTTP response support
different stages. ARP/DNS cache reuse is plausible but cache history is not
captured.

## Completion Standard

Order the observed stages and label cached-stage assumptions.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which stages may be absent from a capture because of caching?

2. How would a DNS failure differ from a TCP refusal in the evidence?

3. Did you separate user-visible symptoms from the failing dependency?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1034 §§4–5 — name servers and resolvers](https://www.rfc-editor.org/rfc/rfc1034.html)

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
