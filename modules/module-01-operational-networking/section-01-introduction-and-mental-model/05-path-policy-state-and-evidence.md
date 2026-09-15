# Path, Policy, State, and Evidence

> **Module 1 · Section 1**

## Why It Matters

Most network questions become manageable when decomposed into four parts: where
traffic can go, whether it is allowed, what state it depends on, and what
observations prove the conclusion.

## Core Model

* Path is the sequence of forwarding decisions from source to destination and
  back.

* Policy determines permitted behavior through ACLs, firewalls, proxies,
  routing filters, and endpoint controls.

* State includes neighbor entries, routes, NAT mappings, transport connections,
  authentication, and middlebox sessions.

* Evidence is an observation with a source, collection point, timestamp, and
  known limitation.

* A conclusion is strongest when path, policy, state, and evidence agree;
  disagreement identifies the next investigation target.

## Reasoning Process

1. Write the expected forward and return paths.

2. At each boundary, identify the forwarding decision, policy check, and
   required state.

3. List the evidence expected from endpoints, network devices, and sensors.

4. Label every claim as observed, inferred, hypothesized, or unknown.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether the intended external deny agrees
with the incident firewall decision.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

F2 intends deny; firewall record 1 allows the external flow using
TEMP-EGRESS-17. A design intention and a later observed decision can differ.

## Completion Standard

Write intent, observation, and a change-owner question separately.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why does a permitted policy not prove a usable path exists?

2. Which state can make one direction work while the reverse initiation fails?

3. What evidence would distinguish a routing failure from a policy denial?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
