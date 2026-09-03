# Network Engineer Perspective

> **Module 3 · Section 5**

## Why It Matters

The network engineer determines whether packets can traverse the modeled
infrastructure and which forwarding, state, and failure conditions explain the
observations.

## Core Model

* Reachability requires valid endpoint configuration, VLAN or segment
  attachment, routes, next hops, and return paths.

* VRFs and overlapping contexts determine which routes are eligible.

* Firewalls, NAT, tunnels, and load balancers create state and tuple
  transformations that affect forwarding.

* ECMP, high availability, and circuit failover can create transient or
  persistent asymmetry.

* Operational evidence includes route, neighbor, interface, session,
  translation, and packet facts.

## Reasoning Process

1. Resolve source and destination context, address, route, next hop, and egress
   at each boundary.

2. Trace return routes and stateful-device ownership.

3. Compare the observed tuple with transformations and capture locations.

4. Test failure, convergence, asymmetry, and stale-state explanations.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop
   touch work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/02-network-engineer-perspective.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Network Engineer Perspective** in
   `work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/02-network-engineer-perspective.md`.
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
`work/module-03-incident-response-and-integration/section-05-integrated-architecture-and-incident-tabletop/02-network-engineer-perspective.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Which VRF contains the relevant prefix?

2. Could the observation arise from a different return path?

3. What table or session output would most strongly test the path?
