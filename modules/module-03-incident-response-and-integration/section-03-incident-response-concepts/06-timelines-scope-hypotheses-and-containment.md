# Timelines, Scope, Hypotheses, and Containment

> **Module 3 · Section 3**

## Why It Matters

A defensible investigation maintains a normalized timeline, explicit case
definition, competing explanations, calibrated confidence, and proportionate
action.

## Core Model

* A normalized timeline preserves original timestamps and records conversion,
  precision, and clock uncertainty.

* A case definition states which observations qualify an asset, identity, or
  event as in scope.

* A hypothesis must predict evidence and remain falsifiable.

* Confidence reflects evidence quality and alternatives, not analyst
  conviction.

* Containment reduces risk but can destroy evidence, interrupt operations,
  expose the investigation, or create safety consequences.

## Reasoning Process

1. Normalize source time while preserving raw values and provenance.

2. Define scope criteria, then search consistently for matching and
   near-matching entities.

3. Maintain at least one plausible alternative hypothesis and test predictions.

4. Choose containment using threat, impact, confidence, reversibility, evidence
   preservation, and owner approval.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-03-incident-response-concepts
   touch work/module-03-incident-response-and-integration/section-03-incident-response-concepts/06-timelines-scope-hypotheses-and-containment.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Timelines, Scope, Hypotheses, and Containment** in
   `work/module-03-incident-response-and-integration/section-03-incident-response-concepts/06-timelines-scope-hypotheses-and-containment.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq -c '.' labs/fixtures/incident/siem.jsonl
   jq -c '.' labs/fixtures/incident/endpoint.jsonl
   jq -c '.' labs/fixtures/incident/auth.jsonl
   jq -c '.' labs/fixtures/incident/flows.jsonl
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for **Timelines,
   Scope, Hypotheses, and Containment**. Apply the numbered Reasoning Process in
   order. Tie every claim to a frame or log record and label it observed,
   inferred, hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `source`, `raw time`,
   `normalized time`, `entity`, `observation`, `classification`, `limitation`,
   and `confidence`. Cite exact frames or records.

6. Apply every step in the Reasoning Process, answer all Check Your
   Understanding questions, and keep at least one plausible alternative
   hypothesis in the same output file.

## Expected Evidence

* The SIEM alert is created at `16:04:10Z` by `WORKSTATION-SMB-FANOUT`; it is
  an alert, not proof of an incident.

* Endpoint evidence places `update-agent` before `smb-client`, and
  authentication records a successful `svc-backup` network login to `file-01`
  from `10.0.10.23`.

* The evidence supports external periodic TLS and successful access to one SMB
  service, but it does not prove credential theft, remote execution,
  persistence, or data exfiltration.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-03-incident-response-concepts/06-timelines-scope-hypotheses-and-containment.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Why should original timestamps be preserved?

2. What makes a scope definition reproducible?

3. When is delayed containment more defensible than immediate isolation?
