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

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop
   touch work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/05-incident-responder-perspective.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Incident Responder Perspective** in
   `work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/05-incident-responder-perspective.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq '.' labs/fixtures/routing/vrfs.json
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   jq -c '.' labs/fixtures/incident/auth.jsonl
   jq -c '.' labs/fixtures/incident/endpoint.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for **Incident
   Responder Perspective**. Apply the numbered Reasoning Process in order. Tie
   every claim to a frame or log record and label it observed, inferred,
   hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `source`, `raw time`,
   `normalized time`, `entity`, `observation`, `classification`, `limitation`,
   and `confidence`. Cite exact frames or records.

6. Apply every step in the Reasoning Process, answer all Check Your
   Understanding questions, and keep at least one plausible alternative
   hypothesis in the same output file.

## Expected Evidence

* The reference policy permits enterprise server `10.0.20.40` to reach the OT
  historian but denies direct user-workstation access.

* The observed SMB access crosses only the CORP user/server boundary, while the
  later direct user-to-OT HTTPS attempt is denied.

* The four disciplines should agree on the factual path and timestamps while
  producing different but compatible decisions about design, control, scope,
  and action.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/05-incident-responder-perspective.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Which claim currently has the weakest source quality?

2. How was incident scope defined?

3. What containment action could endanger operations or destroy evidence?
