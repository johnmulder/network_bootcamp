# Translating Across Disciplines

> **Module 3 · Section 6**

## Why It Matters

Cross-functional communication succeeds when specialized observations are
translated into shared packet, boundary, state, and evidence terms without
erasing important nuance.

## Core Model

* Network engineering language emphasizes paths, tables, interfaces, protocols,
  and state.

* Architecture language emphasizes intent, boundaries, dependencies, failure
  domains, and tradeoffs.

* Security engineering language emphasizes policy, trust, prevention,
  detection, and exposure.

* Incident response language emphasizes evidence, timeline, scope, confidence,
  and action.

* A good translation preserves the original claim, identifies inference, and
  adds the context needed for another discipline to test it.

## Reasoning Process

1. Quote or restate the original observation without interpretation.

2. Define specialized terms and identify the observation point.

3. Translate the claim into path, policy, state, and evidence.

4. State the high-value question for each other discipline.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Translate TEMP-EGRESS-17 without turning a rule
decision into a compromise finding.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

Engineering sees an allowed translated tuple; security sees a deviation from
intent; response still lacks malicious purpose. Each perspective must preserve
the same record.

## Completion Standard

Produce three plain-language translations with the same certainty.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What information is lost when “blocked” is translated as “unreachable”?

2. How does a failure domain differ from incident scope?

3. Which terms should remain precise rather than simplified?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
