# Joint Cross-Functional Assessment

> **Module 3 · Section 5**

## Why It Matters

The integrated output reconciles engineering, architecture, security, and
response views into one shared path, fact set, risk statement, and action plan.

## Core Model

* All disciplines should agree on endpoint identities, tuples, path,
  boundaries, timestamps, and evidence provenance.

* Disagreement should be expressed as a specific assumption or unresolved fact
  rather than disciplinary terminology.

* Immediate containment, service restoration, evidence collection, and
  long-term remediation have different owners and priorities.

* Actions can conflict, such as preserving a path for observation versus
  blocking it for safety.

* The final plan must name decision authority, prerequisites, sequence,
  validation, and rollback.

## Reasoning Process

1. Merge the four assessments and identify factual agreements and conflicts.

2. Resolve terminology and test conflicts against source evidence.

3. Prioritize actions by threat, operational consequence, reversibility, and
   information value.

4. Publish one shared packet path, boundary map, evidence summary, and action
   register.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict where engineering, security, and response
might disagree despite reading the same facts.

Run from the repository root:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/incident/firewall.jsonl
jq '.' labs/fixtures/incident/auth.jsonl
```

## Expected Evidence and Worked Reasoning

Intent, observed permit, and recorded login are different claims. A shared
action can preserve evidence and review the exception without inventing remote
execution.

## Completion Standard

Write one agreed fact, one disputed assumption, and an owned next step.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which disagreement is factual rather than semantic?

2. Do immediate and long-term actions have distinct objectives?

3. Can every stakeholder verify the facts underlying the plan?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
