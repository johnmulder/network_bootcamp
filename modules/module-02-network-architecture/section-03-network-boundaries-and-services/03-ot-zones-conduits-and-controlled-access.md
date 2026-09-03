# OT Zones, Conduits, and Controlled Access

> **Module 2 · Section 3**

## Why It Matters

Operational technology networks prioritize safe and reliable physical
processes. Their segmentation and access patterns must reflect consequence,
lifecycle, and protocol constraints.

## Core Model

* Zones group assets with similar function, criticality, and security
  requirements; conduits define controlled communication between zones.

* An industrial DMZ separates enterprise services from supervisory and control
  networks and hosts approved transfer functions.

* Jump hosts and controlled remote-access paths concentrate authentication,
  recording, and policy enforcement.

* PLCs, IEDs, HMIs, historians, and engineering workstations have different
  communication and availability needs.

* Safety, deterministic operation, long equipment lifecycles, and limited
  maintenance windows constrain containment and scanning.

## Reasoning Process

1. Identify the physical process and the systems that observe or control it.

2. Group assets by function and consequence rather than IP range alone.

3. Define required conduits and prohibit direct paths that bypass the
   industrial DMZ.

4. Evaluate maintenance, vendor access, monitoring, failure, and safe recovery.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-03-network-boundaries-and-services
   touch work/module-02-network-architecture/section-03-network-boundaries-and-services/03-ot-zones-conduits-and-controlled-access.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **OT
   Zones, Conduits, and Controlled Access** in
   `work/module-02-network-architecture/section-03-network-boundaries-and-services/03-ot-zones-conduits-and-controlled-access.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq 'to_entries[] | {component: .key, behavior: .value}' labs/fixtures/architecture/components.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **OT Zones,
   Conduits, and Controlled Access**. Apply the numbered Reasoning Process in
   order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* User-to-server HTTP is allowed at `core-acl`, direct user-to-OT HTTPS is
  denied at `ot-firewall-a`, and management SSH requires `jump-host-policy`.

* The enterprise firewall routes, modifies, enforces policy, maintains state,
  and logs sessions, NAT, and denies, but does not terminate TLS.

* The reverse proxy and load balancer terminate TLS and create server-side
  behavior that a simple firewall or IDS does not.

## Completion Standard

Submit
`work/module-02-network-architecture/section-03-network-boundaries-and-services/03-ot-zones-conduits-and-controlled-access.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why can aggressive containment be unsafe in an OT environment?

2. What function does an industrial DMZ serve?

3. Which access should require a jump host and session recording?
