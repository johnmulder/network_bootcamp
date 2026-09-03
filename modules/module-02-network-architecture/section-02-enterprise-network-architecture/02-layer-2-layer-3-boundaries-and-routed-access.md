# Layer 2, Layer 3 Boundaries, and Routed Access

> **Module 2 · Section 2**

## Why It Matters

Boundary placement determines broadcast scope, convergence behavior, traffic
paths, and where policy or telemetry can be applied.

## Core Model

* Extending Layer 2 permits mobility and shared subnets but enlarges broadcast
  and spanning-tree failure domains.

* A Layer 3 boundary contains broadcasts and provides an explicit route and
  policy decision.

* Traditional access designs often route at distribution, while routed access
  places Layer 3 closer to access switches.

* First-hop gateway placement influences failure behavior and east-west paths.

* Boundary choice affects troubleshooting because it determines which tables
  and protocols decide forwarding.

## Reasoning Process

1. Mark every broadcast domain and default-gateway location.

2. Determine how far each VLAN extends and which links are routed.

3. Compare convergence and blast radius for a link, switch, or gateway failure.

4. Choose boundary placement based on endpoint, mobility, policy, and
   operational requirements.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-02-enterprise-network-architecture
   touch work/module-02-network-architecture/section-02-enterprise-network-architecture/02-layer-2-layer-3-boundaries-and-routed-access.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Layer
   2, Layer 3 Boundaries, and Routed Access** in
   `work/module-02-network-architecture/section-02-enterprise-network-architecture/02-layer-2-layer-3-boundaries-and-routed-access.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   jq '.stp' labs/fixtures/network/l2-control.json
   jq -c '.' labs/fixtures/architecture/failures.jsonl
   ```

4. In the output file, add a `## Architecture Analysis` section for **Layer 2,
   Layer 3 Boundaries, and Routed Access**. Apply the numbered Reasoning Process
   in order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The reference architecture separates user, server, management, OT DMZ, and
  supervisory roles rather than representing one flat failure domain.

* `sw-dist-1` is the modeled spanning-tree root and one access-to-access path
  is non-forwarding.

* The failure data distinguishes endpoint isolation, stale firewall session
  synchronization, degraded WAN transport, and a stale DNS answer.

## Completion Standard

Submit
`work/module-02-network-architecture/section-02-enterprise-network-architecture/02-layer-2-layer-3-boundaries-and-routed-access.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. What problem does routed access reduce?

2. Why might a design still extend Layer 2?

3. How does moving the gateway change an east-west packet path?
