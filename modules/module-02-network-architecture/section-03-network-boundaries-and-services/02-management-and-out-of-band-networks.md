# Management and Out-of-Band Networks

> **Module 2 · Section 3**

## Why It Matters

Management access can change the network and therefore needs stronger
separation, identity, resilience, and monitoring than ordinary user traffic.

## Core Model

* An in-band management path shares production forwarding, while out-of-band
  management uses a separate path or interface.

* Out-of-band access can support recovery during production failures but can
  also become a high-impact attack path.

* Management networks require controlled entry, strong authentication, least
  privilege, logging, and protected name and time services.

* Console servers, jump hosts, automation systems, monitoring platforms, and
  administrators are all part of the management architecture.

* Emergency access must be tested without turning permanent bypass into normal
  practice.

## Reasoning Process

1. Inventory every way a device can be administered.

2. Trace identity, transport, and authorization from administrator to device.

3. Separate routine, automated, emergency, and vendor access paths.

4. Evaluate operation during loss of production routing, DNS, authentication,
   or the management network itself.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-03-network-boundaries-and-services
   touch work/module-02-network-architecture/section-03-network-boundaries-and-services/02-management-and-out-of-band-networks.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Management and Out-of-Band Networks** in
   `work/module-02-network-architecture/section-03-network-boundaries-and-services/02-management-and-out-of-band-networks.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq 'to_entries[] | {component: .key, behavior: .value}' labs/fixtures/architecture/components.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Management
   and Out-of-Band Networks**. Apply the numbered Reasoning Process in order.
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
`work/module-02-network-architecture/section-03-network-boundaries-and-services/02-management-and-out-of-band-networks.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why is an out-of-band network still a security risk?

2. What services must management access survive without?

3. Where should administrative actions be logged?
