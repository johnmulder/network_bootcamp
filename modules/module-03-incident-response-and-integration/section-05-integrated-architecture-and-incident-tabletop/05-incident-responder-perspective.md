# Incident Responder Perspective

> **Module 3 · Section 5**

## Why It Matters

The incident responder reconstructs what happened, what remains unknown, how
far activity extends, and what action reduces risk without overstating
evidence.

## Core Model

* Facts are observations with provenance; interpretations connect facts;
  hypotheses remain testable explanations.

* Scope covers assets, identities, data, techniques, infrastructure, and time
  using explicit criteria.

* Missing telemetry can limit confidence and change containment choice.

* Containment objectives differ from eradication and long-term remediation.

* OT response may require coordination with process owners before isolation or
  scanning.

## Reasoning Process

1. Build the normalized timeline and evidence ledger.

2. Evaluate competing hypotheses and assign claim-level confidence.

3. Apply the case definition to search for related activity and negative
   findings.

4. Recommend evidence collection and containment with risk, owner, validation,
   and rollback.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict a proportionate containment decision without
claiming unobserved credential theft.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/auth.jsonl
jq '.' labs/fixtures/incident/endpoint.jsonl
```

## Expected Evidence and Worked Reasoning

Recorded authentication and process evidence justify investigation but do not
settle malicious intent. The OT process owner must approve actions affecting
the stated monitoring dependency.

## Completion Standard

Separate evidence collection, containment goal, and recovery criterion.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which claim currently has the weakest source quality?

2. How was incident scope defined?

3. What containment action could endanger operations or destroy evidence?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)

[NIST SP 800-82r3 — OT topologies and security architecture](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
