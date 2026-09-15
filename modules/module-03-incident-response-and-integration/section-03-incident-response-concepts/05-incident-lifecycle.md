# Incident Lifecycle

> **Module 3 · Section 3**

## Why It Matters

The incident lifecycle organizes work from detection through recovery and
learning. Phases can overlap and repeat as evidence changes.

## Core Model

* Preparation establishes ownership, available evidence, approved actions,
  recoverable configurations, and practiced procedures before detection.

* Detection identifies behavior requiring attention; triage establishes
  validity, priority, and immediate risk.

* Investigation develops timelines and hypotheses; scoping identifies affected
  identities, assets, data, and time.

* Containment limits ongoing harm while considering business and safety
  consequences.

* Eradication removes the mechanism and persistence after scope is credible.

* Recovery restores service safely and monitors for recurrence.

* Lessons learned improve architecture, controls, telemetry, procedures, and
  ownership.

Investigation, scoping, and containment can overlap. New evidence may reopen
an earlier decision. The course sequence is a teaching aid, not NIST's fixed
eight-step lifecycle; see the
[NIST mapping and recovery epilogue](../../../challenges/recovery.md#preparation-and-feedback).

## Reasoning Process

1. Define current phase objectives and decision authority.

2. Maintain a shared fact set, timeline, scope, and action log.

3. Choose containment proportional to evidence, impact, and operational risk.

4. Verify eradication and recovery against explicit success criteria before
   closure.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Assume a newly detected suspicious flow while the
process owner reports a critical monitoring dependency. Choose overlapping
preparation, investigation, containment, and recovery work.

This is a conceptual exercise under the assumptions above; no device
configuration or observed takeover/fabric state is supplied.

## Expected Evidence and Worked Reasoning

Ownership, retained telemetry, and approved actions shape response before an
alert. Containment may run alongside scoping. Restoration needs a service
test; eradication needs evidence of removed malicious mechanisms.

## Completion Standard

Explain preparation and a feedback loop; do not call the course sequence
NIST's fixed lifecycle.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can containment begin before investigation is complete?

2. What makes recovery different from eradication?

3. When should scoping be revisited?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
