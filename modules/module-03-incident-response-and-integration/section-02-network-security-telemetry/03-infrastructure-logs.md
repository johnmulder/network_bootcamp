# Infrastructure Logs

> **Module 3 · Section 2**

## Why It Matters

DNS, DHCP, firewall, proxy, VPN, and authentication logs provide semantic
context unavailable in raw packets, but each reflects one product's decision
and logging policy.

## Core Model

* DNS logs connect clients, names, record types, answers, and resolver
  behavior, subject to cache and encrypted-resolution gaps.

* DHCP logs help map dynamically assigned addresses to clients over time.

* Firewall logs describe rule and session decisions at one boundary, often
  using translated tuples.

* Proxy logs can expose URLs, users, policy, and server outcomes when traffic
  actually traverses the proxy.

* VPN and authentication logs connect remote addresses, assigned addresses,
  identities, devices, factors, and session timing.

## Reasoning Process

1. Document log source, collection point, fields, time zone, retention, and
   logging conditions.

2. Normalize identifiers and timestamps before correlation.

3. Distinguish an attempted action, a policy decision, an established session,
   and successful application use.

4. Cross-check identity and address claims against lease, VPN, endpoint, and
   translation evidence.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which infrastructure source can explain
translation, bypass, and remote assignment.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/firewall.jsonl
jq '.' labs/fixtures/incident/proxy.jsonl
jq '.' labs/fixtures/incident/vpn.jsonl
```

## Expected Evidence and Worked Reasoning

Firewall records the translated address, proxy records BYPASS, and VPN records
a separate contractor address. They describe different identities and
boundaries.

## Completion Standard

Cite one field per source and reject unsupported identity joins.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Does a firewall allow log prove application success?

2. Why can a DNS cache create no new resolver log for a connection?

3. Which records are needed to map a VPN-assigned address to a user at one
   time?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 3022 §2 — traditional NAT terminology](https://www.rfc-editor.org/rfc/rfc3022.html#section-2)

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
