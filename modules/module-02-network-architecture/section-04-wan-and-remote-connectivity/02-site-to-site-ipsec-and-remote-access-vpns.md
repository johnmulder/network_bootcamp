# Site-to-Site IPsec and Remote-Access VPNs

> **Module 2 · Section 4**

## Why It Matters

VPNs add encrypted overlays across untrusted transport. They create new
interfaces, routes, identities, policy stages, MTU constraints, and observation
points.

## Core Model

* IPsec commonly uses IKE to authenticate peers and negotiate security
  associations for protected traffic.

* Selectors or route-based interfaces determine which traffic enters a
  site-to-site tunnel.

* Remote-access VPNs authenticate users or devices and assign addresses,
  routes, DNS, and policy.

* Split tunneling sends selected traffic outside the tunnel, while full
  tunneling directs it through the VPN.

* Encapsulation adds overhead, changes MTU, and limits what intermediate
  sensors can observe.

## Reasoning Process

1. Separate the public underlay path from the protected overlay path.

2. Identify peer or user authentication, selectors, assigned routes, and
   policy.

3. Calculate where encryption begins and ends and which tuple each sensor sees.

4. Test tunnel loss, rekey, overlapping addresses, return routing, and MTU.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-04-wan-and-remote-connectivity
   touch work/module-02-network-architecture/section-04-wan-and-remote-connectivity/02-site-to-site-ipsec-and-remote-access-vpns.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Site-to-Site IPsec and Remote-Access VPNs** in
   `work/module-02-network-architecture/section-04-wan-and-remote-connectivity/02-site-to-site-ipsec-and-remote-access-vpns.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/architecture/wan.json
   jq '.circuits[] | {name, provider, state, loss_percent, capacity_mbps, preference}' labs/fixtures/architecture/wan.json
   jq '.routes, .sdwan_policy, .mpls' labs/fixtures/architecture/wan.json
   ```

4. In the output file, add a `## Architecture Analysis` section for
   **Site-to-Site IPsec and Remote-Access VPNs**. Apply the numbered Reasoning
   Process in order. Tie every design or failure claim to a named component,
   boundary, route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* `private-1` is preferred but degraded with 20 percent loss; `internet-vpn-1`
  is up, lower capacity, and encrypted.

* The branch default still points through HQ on the degraded private circuit,
  while the specific HQ prefix uses the VPN fixture.

* The MPLS service is provider-managed private routing but is explicitly not
  encrypted; SD-WAN policy chooses paths by application intent.

## Completion Standard

Submit
`work/module-02-network-architecture/section-04-wan-and-remote-connectivity/02-site-to-site-ipsec-and-remote-access-vpns.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Can the tunnel be up while application traffic fails?

2. Why does split tunneling change security visibility?

3. Which MTU problem can encapsulation introduce?
