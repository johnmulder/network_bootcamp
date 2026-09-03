# Network Architect Perspective

> **Module 3 · Section 5**

## Why It Matters

The network architect evaluates why boundaries exist, how dependencies and
failures shape risk, and whether the observed incident exposes a design
weakness.

## Core Model

* Trust and security boundaries should follow communication and consequence
  requirements.

* Failure domains include shared management, identity, control, software,
  facility, and provider dependencies.

* Redundancy must preserve policy, state, capacity, visibility, and safe
  recovery.

* Blast radius depends on route reachability, shared credentials, permitted
  conduits, and administrative control.

* An incident can reveal drift or misuse without proving the original
  architecture intent was wrong.

## Reasoning Process

1. Restate design requirements and intended communication.

2. Map trust, failure, management, visibility, and ownership boundaries.

3. Evaluate how the suspected path bypassed, crossed, or used those boundaries.

4. Recommend the smallest architecture improvement that reduces recurrence or
   blast radius.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop
   touch work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/03-network-architect-perspective.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Network Architect Perspective** in
   `work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/03-network-architect-perspective.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Network
   Architect Perspective**. Apply the numbered Reasoning Process in order. Tie
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
`work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/03-network-architect-perspective.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Which boundary failed to contain the suspected behavior?

2. Was the weakness architectural, configurational, operational, or
   evidentiary?

3. What change reduces risk without creating disproportionate complexity?
