# NetFlow and IPFIX

> **Module 3 · Section 2**

## Why It Matters

Flow telemetry summarizes communications at much lower storage cost than packet
capture. It is powerful for scope and pattern analysis but omits payload and
often detailed protocol state.

## Core Model

* A flow record commonly includes source and destination addresses, ports,
  protocol, timestamps, counters, interfaces, and exporter context.

* Unidirectional records mean one conversation can produce separate forward and
  reverse entries.

* Active and inactive timeouts split long communication into multiple records.

* Sampling, aggregation, exporter placement, NAT, and templates affect
  precision and interpretation.

* Flow evidence can establish observed tuple, timing, and volume at an exporter
  but not application content or endpoint process.

## Reasoning Process

1. Identify exporter, observation domain, interfaces, template, sampling, and
   time basis.

2. Normalize records into forward and reverse groups using tuple and timing.

3. Account for timeout splits, NAT stages, duplicate exporters, and missing
   records.

4. Use patterns such as periodicity, fan-out, duration, and bytes as hypotheses
   rather than verdicts.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether repeated TCP/443 tuples identify the
source process.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/flows.jsonl
```

## Expected Evidence and Worked Reasoning

Three external summaries have periodic starts, but no process-to-socket
attribution or payload. Exporter sampling/placement must not be invented.

## Completion Standard

Measure periodicity and separate tuple evidence from process attribution.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can one TCP connection appear as several flow records?

2. What can byte counters suggest but not prove?

3. How does exporter location affect attribution through NAT?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 7011 §2 — IPFIX observation and metering](https://www.rfc-editor.org/rfc/rfc7011.html#section-2)
