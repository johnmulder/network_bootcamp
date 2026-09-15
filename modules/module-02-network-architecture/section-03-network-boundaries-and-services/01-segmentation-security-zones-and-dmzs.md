# Segmentation, Security Zones, and DMZs

> **Module 2 · Section 3**

## Why It Matters

Segmentation limits reachability and blast radius by placing explicit
boundaries between systems with different trust, exposure, ownership, or
operational requirements.

## Core Model

* A segment is a forwarding scope; a security zone groups systems for policy
  based on trust or function.

* A DMZ hosts services that must interact across trust boundaries without
  placing them directly inside a protected network.

* Segmentation can use VLANs, VRFs, routed links, firewalls, host controls, or
  combinations of them.

* Zone names do not enforce policy; traffic must traverse a known control point
  with explicit rules.

* Shared services and management paths can bypass intended segmentation if they
  are not modeled.

## Reasoning Process

1. Group assets by communication need, trust, exposure, ownership, and
   consequence.

2. Define allowed flows before selecting the technical boundary.

3. Place enforcement so all relevant paths, including return and management
   paths, cross it.

4. Test bypass, failure, shared-service, and recovery behavior.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-03-network-boundaries-and-services
   touch work/module-02-network-architecture/section-03-network-boundaries-and-services/01-segmentation-security-zones-and-dmzs.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Segmentation, Security Zones, and DMZs** in
   `work/module-02-network-architecture/section-03-network-boundaries-and-services/01-segmentation-security-zones-and-dmzs.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq 'to_entries[] | {component: .key, behavior: .value}' labs/fixtures/architecture/components.json
   ```

4. In the output file, add a `## Architecture Analysis` section for
   **Segmentation, Security Zones, and DMZs**. Apply the numbered Reasoning
   Process in order. Tie every design or failure claim to a named component,
   boundary, route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The flow matrix intends user-to-server HTTP to be permitted at `core-acl`,
  user-to-OT HTTPS denied at `ot-firewall-a`, and management SSH controlled
  by `jump-host-policy`. These intentions do not prove an installed rule,
  an available route, or a successful session.

* In this component model, the enterprise firewall routes, modifies,
  enforces policy, maintains state,
  and logs sessions, NAT, and denies, but does not terminate TLS.

* The modeled reverse proxy and load balancer terminate TLS and create server-side
  behavior that a simple firewall or IDS does not.

## Completion Standard

Submit
`work/module-02-network-architecture/section-03-network-boundaries-and-services/01-segmentation-security-zones-and-dmzs.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. What distinguishes a security zone from a VLAN?

2. Why is a DMZ not automatically trusted?

3. How can a shared service weaken segmentation?
