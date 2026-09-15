# C2, Beaconing, Discovery, and Credential Access

> **Module 3 · Section 3**

## Why It Matters

Early post-compromise behavior can appear as external command and control,
periodic communication, internal enumeration, and attempts to obtain
credentials.

## Core Model

* Command and control is communication used to direct or manage compromised
  systems; it can use common protocols and services.

* Beaconing is repeated communication with timing or size regularity, but
  software updates and monitoring can look similar.

* Discovery gathers information about hosts, accounts, services, shares, or
  network structure.

* Credential access seeks passwords, tokens, hashes, tickets, keys, or session
  material.

* Network evidence shows communication patterns and destinations, while
  endpoint evidence is often required to establish command, process, and
  credential actions.

## Reasoning Process

1. Measure timing, tuple, volume, protocol, and destination history for
   suspected C2.

2. Compare periodicity with benign service behavior and endpoint process
   context.

3. Map internal fan-out or service access to plausible discovery goals.

4. Seek endpoint and identity evidence before claiming credential access.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which observation distinguishes an updater
from malicious command traffic.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/flows.jsonl
jq '.' labs/fixtures/incident/endpoint.jsonl
```

## Expected Evidence and Worked Reasoning

Repeated flow timing and update-agent ancestry fit more than one hypothesis.
Socket attribution, approved updater identity, and command content are not
supplied.

## Completion Standard

Keep both explanations and choose one discriminating endpoint record.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Does periodic traffic prove beaconing?

2. Which network pattern can suggest internal discovery?

3. Why is credential access difficult to prove from flow data alone?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[MITRE ATT&CK — Command and Control tactic](https://attack.mitre.org/tactics/TA0011/)

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
