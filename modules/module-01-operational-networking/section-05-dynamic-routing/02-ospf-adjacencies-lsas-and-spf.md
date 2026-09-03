# OSPF Adjacencies, LSAs, and SPF

> **Module 1 · Section 5**

## Why It Matters

OSPF distributes a link-state view within an autonomous system. Each router
builds a database and runs a shortest-path calculation rather than accepting a
neighbor's complete route choice.

## Core Model

* OSPF neighbors discover one another and form adjacencies only when key
  parameters and network conditions agree.

* Link-state advertisements describe topology and prefix information and are
  flooded through an area.

* The link-state database should be consistent among routers in the same area,
  subject to convergence timing.

* SPF calculates a shortest-path tree using interface costs and derives
  candidate routes.

* Areas limit topology scope and support hierarchy, while redistribution
  introduces routes from other sources.

## Reasoning Process

1. Verify neighbor discovery and adjacency prerequisites.

2. Map each LSA to the topology or prefix information it contributes.

3. Build the local router's shortest-path tree and total cost.

4. Explain route installation, ECMP eligibility, area behavior, and failure
   convergence.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-05-dynamic-routing
   touch work/module-01-operational-networking/section-05-dynamic-routing/02-ospf-adjacencies-lsas-and-spf.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **OSPF
   Adjacencies, LSAs, and SPF** in
   `work/module-01-operational-networking/section-05-dynamic-routing/02-ospf-adjacencies-lsas-and-spf.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/routing/ospf.json
   jq '.' labs/fixtures/routing/bgp.json
   jq -c '.' labs/fixtures/routing/route-events.jsonl
   ```

4. In the output file, add a `## Analysis` section for **OSPF Adjacencies, LSAs,
   and SPF**. Apply the numbered Reasoning Process in order. For each step, cite
   at least one exact command result and label the statement as an observation
   or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* OSPF has two equal-cost paths to `10.0.20.0/24`, each with total cost 20.

* The BGP path through peer `192.0.2.2` has higher local preference 200 and is
  preferred despite its longer AS path.

* After the modeled link failure, the remaining OSPF next hop is installed 80
  milliseconds after detection and existing ECMP flows are rehashed.

## Completion Standard

Submit
`work/module-01-operational-networking/section-05-dynamic-routing/02-ospf-adjacencies-lsas-and-spf.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can two routers be neighbors without reaching full adjacency?

2. What information does an LSA carry compared with an installed route?

3. How does area design limit control-plane scope?
