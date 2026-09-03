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

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop
   touch work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/06-joint-cross-functional-assessment.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Joint
   Cross-Functional Assessment** in
   `work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/06-joint-cross-functional-assessment.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Joint
   Cross-Functional Assessment**. Apply the numbered Reasoning Process in order.
   Tie every claim to a frame or log record and label it observed, inferred,
   hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `evidence ID`, `source`,
   `collection point`, `raw time`, `normalized time`, `entity`, `observation`,
   `classification`, `limitation`, and `confidence`. Cite exact frames or
   records.

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
`work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/06-joint-cross-functional-assessment.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Which disagreement is factual rather than semantic?

2. Do immediate and long-term actions have distinct objectives?

3. Can every stakeholder verify the facts underlying the plan?
