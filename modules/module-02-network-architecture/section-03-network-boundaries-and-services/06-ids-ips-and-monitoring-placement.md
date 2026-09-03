# IDS, IPS, and Monitoring Placement

> **Module 2 · Section 3**

## Why It Matters

Detection value depends as much on sensor placement and visibility as on
signatures or analytics. Inline prevention adds enforcement and availability
consequences.

## Core Model

* An IDS observes traffic and generates detections; an IPS is positioned to
  block or alter traffic inline.

* Signature detection matches known patterns, while behavioral methods identify
  deviations or suspicious sequences.

* Encryption, asymmetric paths, packet loss, encapsulation, and overloaded
  sensors reduce visibility.

* Sensor placement should correspond to important trust boundaries and
  investigation questions.

* An inline IPS can prevent traffic but also introduces latency, failure,
  tuning, and bypass considerations.

## Reasoning Process

1. Define the traffic and threat behavior that must be observed.

2. Choose a collection point that sees both directions and the useful stage of
   encryption.

3. Estimate capacity, packet loss, encapsulation, and evasion constraints.

4. Plan alert validation, failure behavior, tuning ownership, and evidence
   retention.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-03-network-boundaries-and-services
   touch work/module-02-network-architecture/section-03-network-boundaries-and-services/06-ids-ips-and-monitoring-placement.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **IDS,
   IPS, and Monitoring Placement** in
   `work/module-02-network-architecture/section-03-network-boundaries-and-services/06-ids-ips-and-monitoring-placement.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq 'to_entries[] | {component: .key, behavior: .value}' labs/fixtures/architecture/components.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **IDS, IPS,
   and Monitoring Placement**. Apply the numbered Reasoning Process in order.
   Tie every design or failure claim to a named component, boundary, route,
   policy, or fixture field.

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
`work/module-02-network-architecture/section-03-network-boundaries-and-services/06-ids-ips-and-monitoring-placement.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why can a well-tuned IDS miss traffic?

2. What new risk appears when detection becomes inline prevention?

3. Where should a sensor sit relative to TLS termination?
