# Endpoint and SIEM Telemetry

> **Module 3 · Section 2**

## Why It Matters

Endpoint telemetry ties network activity to processes, users, files, and host
state. A SIEM aggregates many sources but does not remove the need to
understand source semantics.

## Core Model

* EDR can connect sockets to process trees, command lines, hashes, users,
  files, and response actions.

* Endpoint coverage depends on agent health, platform support, policy,
  privileges, and retention.

* A SIEM normalizes, enriches, searches, and correlates events from multiple
  producers.

* Normalization can rename, drop, or transform fields; ingestion delay and
  collection failure can distort timelines.

* A correlation rule expresses a detection hypothesis and can combine weak
  signals without making them individually stronger evidence.

## Reasoning Process

1. Validate endpoint identity, agent health, policy, clock, and collection
   window.

2. Map network tuples to process, user, ancestry, and file evidence.

3. Trace SIEM fields back to raw source events and ingestion metadata.

4. Separate source fact, enrichment, correlation, analyst interpretation, and
   response action.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether process-to-DNS records attribute
every later external socket to update-agent.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/endpoint.jsonl
jq '.' labs/fixtures/incident/siem.jsonl
```

## Expected Evidence and Worked Reasoning

Endpoint records process ancestry and DNS; SIEM correlation cannot fill the
missing process-to-socket event. Agent-health and exact input-event IDs remain
unknown.

## Completion Standard

State the strongest process claim and request tuple-to-process evidence.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can endpoint telemetry prove a packet crossed a firewall?

2. Why should a SIEM field be traced to its source schema?

3. What does a healthy EDR agent fail to observe?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
