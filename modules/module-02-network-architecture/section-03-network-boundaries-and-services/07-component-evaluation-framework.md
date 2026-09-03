# Component Evaluation Framework

> **Module 2 · Section 3**

## Why It Matters

A repeatable evaluation framework prevents diagrams from becoming inventories
of boxes. Each component should be justified by behavior, dependencies, and
evidence.

## Core Model

* The primary question is what requirement or risk the component addresses.

* Routing, traffic modification, policy, state, encryption, and telemetry are
  separate capabilities.

* Every stateful or terminating component changes failure and evidence
  behavior.

* Management, identity, time, naming, update, and control-plane dependencies
  must be included.

* A component can solve one problem while creating a new choke point, blind
  spot, or shared failure.

## Reasoning Process

1. State the requirement and the component's exact role.

2. Classify its forwarding, transformation, enforcement, state, encryption, and
   telemetry behavior.

3. Trace normal and failed flows through it.

4. Record dependencies, ownership, evidence, bypass, and recovery.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-03-network-boundaries-and-services
   touch work/module-02-network-architecture/section-03-network-boundaries-and-services/07-component-evaluation-framework.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Component Evaluation Framework** in
   `work/module-02-network-architecture/section-03-network-boundaries-and-services/07-component-evaluation-framework.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq 'to_entries[] | {component: .key, behavior: .value}' labs/fixtures/architecture/components.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Component
   Evaluation Framework**. Apply the numbered Reasoning Process in order. Tie
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
`work/module-02-network-architecture/section-03-network-boundaries-and-services/07-component-evaluation-framework.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Can the component route traffic without enforcing security policy?

2. Which component behaviors create separate client and server connections?

3. What evidence is lost if the component fails before logging?
