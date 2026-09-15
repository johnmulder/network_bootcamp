# Completion Criteria and Capstone

> **Module 3 · Section 7**

## Why It Matters

Completion means producing a reproducible, evidence-backed cross-functional
analysis on one Mac—not memorizing every protocol or command.

## Core Model

* The participant traces representative forward and return flows and explains
  forwarding, policy, and state.

* The architecture artifact marks trust, failure, management, and visibility
  boundaries.

* The telemetry analysis states what each source proves, suggests, and cannot
  show.

* The incident narrative separates observations, inference, hypotheses, and
  unknowns.

* The final recommendation identifies the highest-value evidence or
  proportionate containment action.

## Reasoning Process

1. Complete the packet-path trace from Module 1.

2. Complete the architecture annotation and failure assessment from Module 2.

3. Complete the evidence ledger, incident narrative, and joint action plan from
   Module 3.

4. Perform a final provenance, uncertainty, safety, and reproducibility review.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a high factual workbench score
substitutes for an evidence-backed final explanation.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number == 3 || frame.number == 5 || frame.number == 6' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e vlan.id -e tcp.flags
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/incident/auth.jsonl
```

## Expected Evidence and Worked Reasoning

The sources support different path, policy, and identity claims. A finished
artifact still needs mechanism, citations, uncertainty, and an actionable
handoff.

## Completion Standard

Use the course outcome map and seven review anchors; keep independent
attainment separate from completion of reference notes.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Can every major claim be reproduced from a cited local source?

2. Did the analysis independently establish the return path?

3. Is the next action owned, proportionate, testable, and reversible?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
