# ACLs and Stateful Firewalls

> **Module 2 · Section 3**

## Why It Matters

ACLs and firewalls enforce traffic policy at network boundaries. Their
placement, direction, state model, and rule semantics determine what they
actually control.

## Core Model

* An ACL commonly evaluates packet fields independently and in order, with an
  explicit or implicit final action.

* A stateful firewall creates session state and can permit return traffic
  without a separate reverse initiation rule.

* Rules depend on zones, interfaces, address objects, services, identity,
  application detection, and platform behavior.

* Routing generally decides where traffic would go; policy decides whether and
  how it may cross.

* Logging configuration, rule counters, NAT order, and asymmetric paths affect
  evidence.

## Reasoning Process

1. Normalize the observed tuple before and after any translation.

2. Place the packet at a specific interface, zone, direction, and session
   state.

3. Evaluate ordered rules and object contents exactly.

4. Check return traffic, logging, timeout, failover, and bypass behavior.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-03-network-boundaries-and-services
   touch work/module-02-network-architecture/section-03-network-boundaries-and-services/04-acls-and-stateful-firewalls.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **ACLs
   and Stateful Firewalls** in
   `work/module-02-network-architecture/section-03-network-boundaries-and-services/04-acls-and-stateful-firewalls.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq 'to_entries[] | {component: .key, behavior: .value}' labs/fixtures/architecture/components.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **ACLs and
   Stateful Firewalls**. Apply the numbered Reasoning Process in order. Tie
   every design or failure claim to a named component, boundary, route, policy,
   or fixture field.

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
`work/module-02-network-architecture/section-03-network-boundaries-and-services/04-acls-and-stateful-firewalls.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why can a stateful firewall permit a reply without a reverse rule?

2. What facts are missing from the claim that a port is open?

3. How can rule order change the result?
