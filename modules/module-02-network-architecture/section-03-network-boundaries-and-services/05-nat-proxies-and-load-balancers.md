# NAT, Proxies, and Load Balancers

> **Module 2 · Section 3**

## Why It Matters

These services can all change traffic paths or identities, but they operate
differently. Architecture diagrams must show where connections terminate and
new ones begin.

## Core Model

* NAT rewrites packet addresses or ports while generally preserving the
  end-to-end transport connection through state.

* A forward proxy acts on behalf of clients; a reverse proxy acts on behalf of
  servers.

* A load balancer selects a backend and may pass packets, terminate transport,
  or terminate application encryption.

* Proxies and full proxies create separate client-side and server-side
  connections with independent tuples and timing.

* Health checks, persistence, source-address handling, TLS termination, and
  backend routing become service dependencies.

## Reasoning Process

1. Classify the component as translation, packet distribution, transport proxy,
   or application proxy.

2. Write client-side and server-side tuples and mark every termination point.

3. Identify selection, health, persistence, policy, and encryption behavior.

4. Determine which logs can correlate both sides of the transaction.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-03-network-boundaries-and-services
   touch work/module-02-network-architecture/section-03-network-boundaries-and-services/05-nat-proxies-and-load-balancers.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **NAT,
   Proxies, and Load Balancers** in
   `work/module-02-network-architecture/section-03-network-boundaries-and-services/05-nat-proxies-and-load-balancers.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq 'to_entries[] | {component: .key, behavior: .value}' labs/fixtures/architecture/components.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **NAT,
   Proxies, and Load Balancers**. Apply the numbered Reasoning Process in order.
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
`work/module-02-network-architecture/section-03-network-boundaries-and-services/05-nat-proxies-and-load-balancers.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. How does a proxy differ from destination NAT?

2. Where is the original client address preserved or lost?

3. Can a healthy load balancer still send traffic to an unusable application?
