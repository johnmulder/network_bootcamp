# DNS Resolution, Delegation, and Caching

> **Module 1 · Section 4**

## Why It Matters

DNS is a distributed naming system and a frequent hidden dependency. Separating
resolver, authoritative, cache, and transport behavior prevents “DNS problem”
from becoming an unhelpful diagnosis.

## Core Model

* A stub resolver asks a recursive resolver, which may query root, top-level,
  and authoritative servers.

* Delegation uses NS records and glue where needed to direct queries toward
  authoritative servers.

* Answers, negative responses, and failures can be cached according to TTL and
  resolver policy.

* DNS commonly uses UDP but can retry over TCP; modern environments may also
  use encrypted transports.

* An answer can be syntactically successful but operationally wrong because of
  split views, stale caches, search domains, or application-specific
  resolution.

## Reasoning Process

1. Identify the querying process, stub configuration, recursive resolver, name,
   type, and search behavior.

2. Trace referral or cached-answer provenance to an authoritative source.

3. Interpret response code, answer section, TTL, and transport behavior.

4. Compare DNS output with the address the application actually attempted.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the local query/answer reveals the
resolver's referral or cache history.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'dns' -T fields -E header=y -e frame.number -e ip.src -e ip.dst -e dns.qry.name -e dns.qry.type -e dns.flags.response -e dns.flags.rcode -e dns.a -e dns.resp.ttl
```

## Expected Evidence and Worked Reasoning

Frames 3–4 show app.example.test resolving to 10.0.20.40 with TTL 300. They
show neither recursive referrals nor whether the resolver used a cache.

## Completion Standard

State the answer and TTL; label recursive provenance unknown and request
resolver tracing.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What is the difference between `NXDOMAIN` and an empty answer for one record
   type?

2. Why can two clients receive different valid answers for the same name?

3. Does a successful DNS response prove the application reached the returned
   address?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1034 §§4–5 — name servers and resolvers](https://www.rfc-editor.org/rfc/rfc1034.html)

[RFC 2308 §2 — negative DNS responses](https://www.rfc-editor.org/rfc/rfc2308.html#section-2)
