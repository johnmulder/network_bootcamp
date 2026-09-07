# Module 2 — Network Architecture

> **Theme:** Why networks are designed the way they are.

The subsection guides explain technical models and provide local evidence
exercises with submission paths and completion standards. The
[VXLAN/EVPN guide](section-05-modern-data-center-and-cloud-networking/02-underlays-overlays-vxlan-and-evpn.md)
is a conceptual reference with a hypothetical diagram and a self-check.

## One-Day Route

Use these challenge briefs during the six-hour course:

* [Spend Your Resilience Budget](../../challenges/04-resilience-budget.md)

Update the three shared artifacts from the [one-day start](../../challenges/README.md).
The subsection guides below are optional references with worked observations;
their individual submission requirements apply only to extended study.

## Dynamic Practice

Use the [Module 2 Workbench](workbench/README.md) for immediate, scored
architecture decisions using the same fixtures as the subsection guides:

```sh
python3 modules/module-02-network-architecture/workbench/module2_workbench.py demo --seed 7 --limit 8
python3 modules/module-02-network-architecture/workbench/module2_workbench.py run all --seed 23 --limit 10
```

## Section 1 — Architecture Foundation Check

* [Packet-Path Foundation Check](section-01-architecture-foundation-check/01-packet-path-foundation-check.md)

## Section 2 — Enterprise Network Architecture

* [Access, Distribution, Core, and Collapsed Core](section-02-enterprise-network-architecture/01-access-distribution-core-and-collapsed-core.md)
* [Layer 2, Layer 3 Boundaries, and Routed Access](section-02-enterprise-network-architecture/02-layer-2-layer-3-boundaries-and-routed-access.md)
* [First-Hop Redundancy, HSRP, and VRRP](section-02-enterprise-network-architecture/03-first-hop-redundancy-hsrp-and-vrrp.md)
* [High Availability: Active/Active and Active/Passive](section-02-enterprise-network-architecture/04-high-availability-active-active-and-active-passive.md)
* [Failure Domains, Redundancy, and Tradeoffs](section-02-enterprise-network-architecture/05-failure-domains-redundancy-and-tradeoffs.md)

## Section 3 — Network Boundaries and Services

* [Segmentation, Security Zones, and DMZs](section-03-network-boundaries-and-services/01-segmentation-security-zones-and-dmzs.md)
* [Management and Out-of-Band Networks](section-03-network-boundaries-and-services/02-management-and-out-of-band-networks.md)
* [OT Zones, Conduits, and Controlled Access](section-03-network-boundaries-and-services/03-ot-zones-conduits-and-controlled-access.md)
* [ACLs and Stateful Firewalls](section-03-network-boundaries-and-services/04-acls-and-stateful-firewalls.md)
* [NAT, Proxies, and Load Balancers](section-03-network-boundaries-and-services/05-nat-proxies-and-load-balancers.md)
* [IDS, IPS, and Monitoring Placement](section-03-network-boundaries-and-services/06-ids-ips-and-monitoring-placement.md)
* [Component Evaluation Framework](section-03-network-boundaries-and-services/07-component-evaluation-framework.md)

## Section 4 — WAN and Remote Connectivity

* [Multisite WAN and Internet Connectivity](section-04-wan-and-remote-connectivity/01-multisite-wan-and-internet-connectivity.md)
* [Site-to-Site IPsec and Remote-Access VPNs](section-04-wan-and-remote-connectivity/02-site-to-site-ipsec-and-remote-access-vpns.md)
* [MPLS and SD-WAN Concepts](section-04-wan-and-remote-connectivity/03-mpls-and-sd-wan-concepts.md)
* [Redundant Circuits, Routing, and Failover](section-04-wan-and-remote-connectivity/04-redundant-circuits-routing-and-failover.md)

## Section 5 — Modern Data Center and Cloud Networking

* [Leaf/Spine Architecture and Traffic Directions](section-05-modern-data-center-and-cloud-networking/01-leaf-spine-and-traffic-directions.md)
* [Underlays, Overlays, VXLAN, and EVPN](section-05-modern-data-center-and-cloud-networking/02-underlays-overlays-vxlan-and-evpn.md)
* [Cloud Virtual Networks, Routes, and Controls](section-05-modern-data-center-and-cloud-networking/03-cloud-virtual-networks-routes-and-controls.md)
* [Transit Gateways and Hybrid Connectivity](section-05-modern-data-center-and-cloud-networking/04-transit-gateways-and-hybrid-connectivity.md)

## Section 6 — Reading a Network Architecture

* [Diagram Literacy and Boundary Identification](section-06-reading-a-network-architecture/01-diagram-literacy-and-boundary-identification.md)
* [Important Traffic-Flow Analysis](section-06-reading-a-network-architecture/02-important-traffic-flow-analysis.md)
* [Dependencies, Redundancy, and Failure Domains](section-06-reading-a-network-architecture/03-dependencies-redundancy-and-failure-domains.md)
* [Annotated Architecture Output](section-06-reading-a-network-architecture/04-annotated-architecture-output.md)

## Section 7 — Architecture Tabletop

* [Architecture Failure-Analysis Method](section-07-architecture-tabletop/01-failure-analysis-method.md)
* [Failure-Scenario Patterns](section-07-architecture-tabletop/02-failure-scenario-patterns.md)
* [Tabletop Assessment Output](section-07-architecture-tabletop/03-tabletop-assessment-output.md)

## Section 8 — Module 2 Review

* [Module 2 Architecture Assessment Review](section-08-module-review/01-architecture-assessment-review.md)
