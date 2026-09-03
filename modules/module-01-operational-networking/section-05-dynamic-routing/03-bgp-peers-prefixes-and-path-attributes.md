# BGP Peers, Prefixes, and Path Attributes

> **Module 1 · Section 5**

## Why It Matters

BGP exchanges reachable prefixes and policy-bearing path attributes between
peers. It is a path-vector protocol designed for administrative control and
scale.

## Core Model

* An autonomous system is a routing domain with a common external policy,
  identified by an AS number.

* eBGP exchanges routes between autonomous systems; iBGP distributes external
  and other BGP routes within one system.

* `AS_PATH` records traversed systems and supports loop prevention and policy.

* `NEXT_HOP` identifies the address used to reach the advertised prefix and may
  require independent resolution.

* `LOCAL_PREF`, communities, filtering, and other attributes express local or
  coordinated policy.

## Reasoning Process

1. Identify the peer type, session endpoints, address family, and advertised
   prefix.

2. Read the path attributes without assuming the shortest AS path always wins.

3. Resolve the BGP next hop using the underlying routing table.

4. Apply import and export policy in the correct administrative direction.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-05-dynamic-routing
   touch work/module-01-operational-networking/section-05-dynamic-routing/03-bgp-peers-prefixes-and-path-attributes.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **BGP
   Peers, Prefixes, and Path Attributes** in
   `work/module-01-operational-networking/section-05-dynamic-routing/03-bgp-peers-prefixes-and-path-attributes.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/routing/ospf.json
   jq '.' labs/fixtures/routing/bgp.json
   jq -c '.' labs/fixtures/routing/route-events.jsonl
   ```

4. In the output file, add a `## Analysis` section for **BGP Peers, Prefixes,
   and Path Attributes**. Apply the numbered Reasoning Process in order. For
   each step, cite at least one exact command result and label the statement as
   an observation or interpretation.

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
`work/module-01-operational-networking/section-05-dynamic-routing/03-bgp-peers-prefixes-and-path-attributes.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why is an established BGP session not proof that a desired prefix is
   accepted?

2. What role does `AS_PATH` play in loop prevention?

3. Why can an unresolved `NEXT_HOP` invalidate an otherwise preferred route?
