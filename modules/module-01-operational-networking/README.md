# Module 1 — Operational Networking

> **Theme:** How packets actually get from A to B.

Each subsection guide explains the technical model, then provides exact local
commands, expected evidence, a submission path, and a completion standard.

## Section 1 — Introduction and Mental Model

* [Course Objectives and Shared Language](section-01-introduction-and-mental-model/01-course-objectives-and-shared-language.md)
* [Network Engineering vs. Protocol Implementation](section-01-introduction-and-mental-model/02-engineering-vs-protocol-implementation.md)
* [Control, Data, and Management Planes](section-01-introduction-and-mental-model/03-control-data-and-management-planes.md)
* [Frames, Packets, Flows, and Sessions](section-01-introduction-and-mental-model/04-frames-packets-flows-and-sessions.md)
* [Path, Policy, State, and Evidence](section-01-introduction-and-mental-model/05-path-policy-state-and-evidence.md)

## Section 2 — Layer 2 Networking

* [Ethernet and MAC Addressing](section-02-layer-2-networking/01-ethernet-and-mac-addressing.md)
* [MAC Learning, Broadcasts, and ARP](section-02-layer-2-networking/02-mac-learning-broadcast-and-arp.md)
* [VLANs, Access Ports, and 802.1Q Trunks](section-02-layer-2-networking/03-vlans-access-ports-and-trunks.md)
* [Inter-VLAN Forwarding](section-02-layer-2-networking/04-inter-vlan-forwarding.md)
* [Spanning Tree Protocol](section-02-layer-2-networking/05-spanning-tree.md)
* [Link Aggregation and LACP](section-02-layer-2-networking/06-link-aggregation-and-lacp.md)
* [Layer 2 Packet-Path Exercise](section-02-layer-2-networking/07-layer-2-packet-path-exercise.md)

## Section 3 — Layer 3 and Packet Forwarding

* [IPv4 Addressing, CIDR, and Subnets](section-03-layer-3-and-packet-forwarding/01-addressing-cidr-and-subnets.md)
* [IPv6 and Neighbor Discovery](section-03-layer-3-and-packet-forwarding/02-ipv6-and-neighbor-discovery.md)
* [Default Gateways and Routing Tables](section-03-layer-3-and-packet-forwarding/03-gateways-and-routing-tables.md)
* [Longest Prefix, Next Hop, and Default Routes](section-03-layer-3-and-packet-forwarding/04-longest-prefix-next-hop-and-default-routes.md)
* [ECMP and Asymmetric Routing](section-03-layer-3-and-packet-forwarding/05-ecmp-and-asymmetric-routing.md)
* [ICMP, TTL, and Traceroute](section-03-layer-3-and-packet-forwarding/06-icmp-ttl-and-traceroute.md)
* [MTU, Path MTU Discovery, and TCP MSS](section-03-layer-3-and-packet-forwarding/07-mtu-path-mtu-and-tcp-mss.md)
* [NAT and PAT](section-03-layer-3-and-packet-forwarding/08-nat-and-pat.md)
* [Routing-Table Exercise](section-03-layer-3-and-packet-forwarding/09-routing-table-exercise.md)

## Section 4 — Transport, Naming, and Core Services

* [TCP, UDP, Ports, and Sockets](section-04-transport-naming-and-core-services/01-tcp-udp-ports-and-sockets.md)
* [TCP Lifecycle and State](section-04-transport-naming-and-core-services/02-tcp-lifecycle-and-state.md)
* [DNS Resolution, Delegation, and Caching](section-04-transport-naming-and-core-services/03-dns-resolution-delegation-and-caching.md)
* [DHCP Address, Gateway, and DNS Assignment](section-04-transport-naming-and-core-services/04-dhcp-address-gateway-and-dns-assignment.md)
* [TLS Sessions and Encryption Visibility](section-04-transport-naming-and-core-services/05-tls-sessions-and-encryption-visibility.md)
* [Application Dependency-Chain Exercise](section-04-transport-naming-and-core-services/06-application-dependency-chain-exercise.md)

## Section 5 — Dynamic Routing

* [Why Dynamic Routing Exists](section-05-dynamic-routing/01-why-dynamic-routing-exists.md)
* [OSPF Adjacencies, LSAs, and SPF](section-05-dynamic-routing/02-ospf-adjacencies-lsas-and-spf.md)
* [BGP Peers, Prefixes, and Path Attributes](section-05-dynamic-routing/03-bgp-peers-prefixes-and-path-attributes.md)
* [Route Selection, Filtering, and Redistribution](section-05-dynamic-routing/04-route-selection-filtering-and-redistribution.md)
* [Convergence and Route-Advertisement Exercise](section-05-dynamic-routing/05-convergence-and-route-advertisement-exercise.md)

## Section 6 — VRFs and Network Segmentation

* [VRFs and Multiple Routing Tables](section-06-vrfs-and-network-segmentation/01-vrfs-and-multiple-routing-tables.md)
* [Route Isolation and Route Leaking](section-06-vrfs-and-network-segmentation/02-route-isolation-and-route-leaking.md)
* [VRFs vs. VLANs and Segmentation Use Cases](section-06-vrfs-and-network-segmentation/03-vrfs-vs-vlans-and-use-cases.md)
* [VRF Isolation Exercise](section-06-vrfs-and-network-segmentation/04-vrf-isolation-exercise.md)

## Section 7 — Network Troubleshooting

* [Hypothesis-Driven Troubleshooting](section-07-network-troubleshooting/01-hypothesis-driven-troubleshooting.md)
* [Link, VLAN, and Address-Resolution Checks](section-07-network-troubleshooting/02-link-vlan-and-address-resolution-checks.md)
* [Routing, VRF, and Policy Checks](section-07-network-troubleshooting/03-routing-vrf-and-policy-checks.md)
* [Firewall State, NAT, and Return Path](section-07-network-troubleshooting/04-firewall-state-nat-and-return-path.md)
* [DNS and Application Checks](section-07-network-troubleshooting/05-dns-and-application-checks.md)
* [Problem Patterns and Evidence-Bundle Exercise](section-07-network-troubleshooting/06-problem-patterns-and-evidence-bundle.md)

## Section 8 — Module 1 Review

* [Module 1 Packet-Path Review](section-08-module-review/01-packet-path-review.md)
