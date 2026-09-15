# DNS and Application Checks

> **Module 1 · Section 7**

## Why It Matters

After path and transport work, failures can remain in naming, TLS, proxies,
authentication, or application behavior. Testing by IP is useful but does not
reproduce the complete dependency chain.

## Core Model

* An application may use search domains, multiple record types, caches,
  proxies, or service discovery that command-line tests do not.

* A reachable IP with a failing hostname suggests a naming dependency but does
  not identify which resolver stage failed.

* TLS name validation and virtual hosting require the intended hostname even
  when the IP is reachable.

* Application errors can occur after successful TCP and TLS establishment.

* Endpoint and server logs may be required because network evidence cannot show
  encrypted application outcomes.

## Reasoning Process

1. Compare application behavior with direct name and address tests without
   assuming equivalence.

2. Confirm the resolver, answer, cache, and address the application actually
   used.

3. Trace TCP and TLS establishment for that exact destination and hostname.

4. Use endpoint or server evidence to interpret behavior beyond encrypted
   network visibility.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict how NXDOMAIN differs from NOERROR with no
AAAA answers.

Run from the repository root:

```sh
jq '.' labs/fixtures/network/troubleshooting.json
```

## Expected Evidence and Worked Reasoning

D2 reports name nonexistence; D3 has NOERROR, empty AAAA answers, SOA, and no
referral, consistent with NODATA for that type. D4 resolves but returns HTTP
503.

## Completion Standard

Distinguish timeout, name absence, type absence, and application failure.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can connecting by IP produce a different TLS result?

2. What does a completed handshake prove about the application?

3. When is absence from a network capture expected rather than suspicious?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1034 §§4–5 — name servers and resolvers](https://www.rfc-editor.org/rfc/rfc1034.html)

[RFC 2308 §2 — negative DNS responses](https://www.rfc-editor.org/rfc/rfc2308.html#section-2)
