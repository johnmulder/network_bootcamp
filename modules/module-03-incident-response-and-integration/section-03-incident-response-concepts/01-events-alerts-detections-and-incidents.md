# Events, Alerts, Detections, and Incidents

> **Module 3 · Section 3**

## Why It Matters

Incident response depends on precise classification. Raw events, analytic
detections, alerts requiring attention, and confirmed incidents are related but
not interchangeable.

## Core Model

* An event is a recorded occurrence from a system, application, network, or
  security control.

* A detection is logic or analysis that identifies behavior matching a
  hypothesis or rule.

* An alert is a notification or case created for review, often from one or more
  detections.

* An incident is a confirmed or sufficiently credible security event requiring
  coordinated response under defined criteria.

* Triage decides priority and next action; it does not require complete
  root-cause certainty.

## Reasoning Process

1. Identify the raw event and source semantics.

2. Explain the analytic condition that produced the detection.

3. Determine why the detection generated an alert and what context it includes.

4. Apply the organization's incident criteria, impact, confidence, and urgency.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether WORKSTATION-SMB-FANOUT alone meets an
incident definition.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/siem.jsonl
```

## Expected Evidence and Worked Reasoning

The record is an alert at 16:04:10Z with flow/endpoint input labels.
Organization-specific declaration criteria and malicious intent are not
supplied.

## Completion Standard

Separate event, detection, alert, and incident decision authority.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can an alert be valid without representing an incident?

2. Why is an incident not merely a severe alert?

3. What information should triage establish first?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
