# Security Engineer Perspective

> **Module 3 · Section 5**

## Why It Matters

The security engineer evaluates permitted communication, enforcement,
preventive controls, monitoring placement, and opportunities to limit lateral
movement.

## Core Model

* Policy should express required flows with least privilege, explicit
  direction, identity, protocol, and ownership.

* Segmentation works only when all paths cross the intended enforcement point.

* Preventive controls include network policy, identity, endpoint hardening,
  application controls, and controlled administration.

* Detection coverage must align with important paths, encryption stages, and
  likely techniques.

* Containment and remediation should account for state, dependencies, business
  function, and OT safety.

## Reasoning Process

1. Compare observed or suspected traffic with the approved flow matrix.

2. Locate every preventive and detective control on the path.

3. Identify which control allowed, missed, blocked, or could not observe the
   behavior.

4. Prioritize a policy, endpoint, identity, or monitoring improvement by risk
   reduction.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop
   touch work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/04-security-engineer-perspective.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Security Engineer Perspective** in
   `work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/04-security-engineer-perspective.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Security
   Engineer Perspective**. Apply the numbered Reasoning Process in order. Tie
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
`work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/04-security-engineer-perspective.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. What specifically should prevent lateral movement at this boundary?

2. Which permitted communication is broader than the business need?

3. Where should monitoring occur relative to encryption termination?
