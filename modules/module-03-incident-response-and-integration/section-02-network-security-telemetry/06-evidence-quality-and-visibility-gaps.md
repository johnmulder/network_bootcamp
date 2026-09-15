# Evidence Quality and Visibility Gaps

> **Module 3 · Section 2**

## Why It Matters

Evidence quality determines the strength of every conclusion. Coverage, timing,
loss, transformation, and retention must be evaluated before interpreting
content.

## Core Model

* Collection point defines the traffic or events eligible to be observed.

* Clock synchronization, time zones, timestamp precision, and ingestion delay
  affect ordering.

* Sampling, aggregation, deduplication, filtering, and parser behavior change
  granularity.

* Retention and rollover create historical gaps that cannot be repaired by
  searching harder.

* NAT, proxy, VPN, load-balancer, and tunnel transformations require
  correlation across identities.

* Sensor health and packet or log loss can make absence meaningless.

## Reasoning Process

1. For each source, document coverage, collection mechanics, clock,
   transformations, and retention.

2. Test source health during the relevant interval.

3. Quantify known loss, sampling, or truncation where possible.

4. State how each limitation changes confidence in specific claims.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a missing packet establishes absence
of the corresponding activity.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
jq '.' labs/fixtures/incident/flows.jsonl
```

## Expected Evidence and Worked Reasoning

The small PCAP and flow summaries have different granularity; full collection
coverage and loss measurements are not supplied. Absence depends on sensor
scope and health.

## Completion Standard

Attach a coverage limitation to one negative claim.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. When is absence of evidence meaningful?

2. How can clock skew reverse the apparent order of events?

3. Which transformation prevents direct tuple matching?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)

[RFC 7011 §2 — IPFIX observation and metering](https://www.rfc-editor.org/rfc/rfc7011.html#section-2)
