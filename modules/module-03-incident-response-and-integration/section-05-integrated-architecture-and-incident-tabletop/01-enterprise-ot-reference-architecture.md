# Enterprise/OT Reference Architecture

> **Module 3 · Section 5**

## Why It Matters

The integrated tabletop applies one incident to an architecture spanning
internet edge, DMZ, enterprise, OT DMZ, supervisory, cell or area, and
controller zones.

## Core Model

* Each boundary has distinct routing, policy, trust, state, management, and
  telemetry behavior.

* The enterprise and OT environments have different availability, safety,
  lifecycle, and response constraints.

* Industrial DMZ services should mediate necessary data and administrative
  exchange.

* Protected-network access may traverse multiple firewalls and independent
  identity or jump-host controls.

* Diagram lines must be converted into explicit paths and conduits before
  incident claims are evaluated.

## Reasoning Process

1. Label every zone, conduit, gateway, firewall, service, and management entry.

2. Define permitted enterprise-to-OT and OT-to-enterprise flows.

3. Trace the suspected activity in both directions through each routing and
   policy context.

4. Map telemetry, ownership, failure, and containment authority to every
   boundary.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop
   touch work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/01-enterprise-ot-reference-architecture.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Enterprise/OT Reference Architecture** in
   `work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/01-enterprise-ot-reference-architecture.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Enterprise/OT
   Reference Architecture**. Apply the numbered Reasoning Process in order. Tie
   every claim to a frame or log record and label it observed, inferred,
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
`work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/01-enterprise-ot-reference-architecture.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Which direct path would violate the intended zone model?

2. Where should enterprise identity be translated into controlled OT access?

3. What safety dependency constrains containment?
