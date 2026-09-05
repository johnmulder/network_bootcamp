# Pocket Reference

Use this during challenges. It is a vocabulary aid, not an answer key. The
[module library](../modules/README.md) contains the longer explanations.

## Addresses and Paths

| Item | Meaning | Useful question |
| --- | --- | --- |
| IP address | Network-layer endpoint address within a routing context | Which destination prefix matches? |
| Prefix / CIDR | Network bits plus prefix length | Is the destination local or routed? |
| `/24` | In these IPv4 examples, the first three octets identify the subnet | Are `10.0.10.23` and `10.0.10.53` in the same subnet? |
| `/32` and `/0` | One IPv4 host; default route | Is a more-specific installed route present? |
| MAC address | Link-layer address used for a local delivery step | Peer MAC or next-hop MAC? |
| ARP / Neighbor Discovery | Resolve IPv4 / IPv6 neighbors on a link | Which neighbor entry is needed? |
| VLAN / VRF | Layer 2 broadcast domain / separate routing table | Which context does this packet actually enter? |
| Longest-prefix match | Choose the most-specific installed destination match | Why do less-specific matches lose? |

A routed packet normally gets a new Ethernet header and a decremented TTL or
Hop Limit. Its endpoint IP addresses normally remain the same unless something
such as NAT changes them. A switch learns source MACs within a VLAN. A router
chooses a next hop using the relevant forwarding table. Return traffic makes
its own decisions. A diagram alone proves none of the current device state.

## Services and Evidence

| Concept | Purpose and limitation |
| --- | --- |
| DHCP | Supplies address, prefix, gateway, and DNS configuration; a lease does not prove service health. |
| DNS | Maps names to records and caches answers; a successful lookup does not establish transport reachability. |
| TCP / UDP | TCP provides an ordered byte stream with connection state; UDP supplies datagrams without TCP's handshake/reliability. Neither guarantees application success. |
| Socket / port | Endpoint address, transport protocol, and port identify a transport endpoint; a port number alone does not identify malicious activity. |
| TLS | Protects application content in transit; a ClientHello is not proof that TLS or the application completed. Some metadata may remain visible, depending on the protocol and deployment. |
| MTU / MSS | IP packet-size limit / advertised TCP payload limit; account for headers and the actual path. |
| ICMP / traceroute | Network feedback / limited path observations; silence is not proof that a router failed. |
| Flow record | Traffic summary; volume or periodicity does not reveal encrypted content. |
| Endpoint / authentication | Process and identity observations; a successful login does not prove how credentials were acquired. |
| Observed / inferred / hypothesized / unknown | Recorded fact / supported interpretation / testable explanation / unanswered question. Confidence belongs to each claim. |

## Recognize the Architecture Vocabulary

Read only the rows needed in the current challenge; revisit the others later.

| Concept | Purpose | Limitation to remember |
| --- | --- | --- |
| STP / LACP | Avoid Layer 2 loops / combine physical links | A redundant link may discard; one flow normally uses one aggregate member. |
| OSPF / BGP | Exchange reachability using topology/cost or routing policy | An adjacency or accepted advertisement does not prove forwarding or application recovery. |
| HSRP / VRRP | Provide first-hop gateway redundancy | Gateway failover does not replicate every firewall or application session. |
| ACL / stateful firewall | Filter packets / enforce rules with connection state | A permitted forward direction alone does not prove return-state continuity. |
| NAT / proxy / load balancer | Translate addresses / mediate requests / distribute service traffic | They can change attribution or create separate connections; inspect the stated behavior. |
| IDS / IPS | Observe and alert / enforce inline | Detection is not proof of an incident; coverage and encrypted visibility matter. |
| DMZ / OT conduit | Bound a service zone / define controlled industrial communications | A boundary label is not proof of enforced rules or complete isolation. |
| Management / out-of-band | Operate equipment / retain an independent access path | Shared power or transport can defeat the claimed independence. |
| IPsec / VPN | Protect traffic between tunnel endpoints | Encryption does not establish correct routes or authorization. |
| MPLS / SD-WAN | Provider forwarding service / application-aware path policy | Private transport is not necessarily encrypted; an up path can perform badly. |
| Leaf/spine | Fabric of access leaves and interconnecting spines | Redundancy still depends on routing, capacity, and failure scope. |
| VXLAN / EVPN | Carry Ethernet frames over an IP underlay / distribute overlay reachability | Underlay reachability does not prove overlay mappings or sufficient MTU. |
| ATT&CK / IOC / TTP | Describe behaviors / suspicious indicator / tactics, techniques, procedures | Naming a technique or matching an indicator does not prove it occurred. |

Use the exact component capabilities in the fixtures; they describe this model,
not every product with the same label. For example, TLS termination and routing
behavior differ among deployed load balancers.
