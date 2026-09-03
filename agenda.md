<!-- markdownlint-configure-file { "MD024": { "siblings_only": true } } -->

# Network Architecture, Engineering, and Incident Response Crash Course

## Course Objective

This course develops practical fluency in the concepts, terminology, artifacts,
and reasoning used by network architects, network engineers, security engineers,
and incident responders.

The emphasis is on understanding and communication rather than vendor-specific
configuration.

At the end of the course, participants should be able to:

* Trace traffic through a network and explain how forwarding decisions are made.
* Interpret and discuss enterprise network architecture diagrams.
* Explain the purpose and basic operation of common routing, segmentation,
  security, and redundancy technologies.
* Identify routing, security, trust, failure, and visibility boundaries.
* Compare major sources of network-security telemetry and state what each can
  prove, suggest, or fail to show.
* Follow an incident-response investigation and distinguish observations,
  inferences, hypotheses, and unknowns.
* Ask useful technical questions of network architects, engineers, and incident
  responders.
* Analyze a network problem from engineering, architecture, security, and
  incident-response perspectives.

## Intended Audience and Prerequisites

This course is for technical professionals who need to collaborate with network
architects, network engineers, security engineers, or incident responders.

No vendor-specific configuration experience is required. Familiarity with IP
addresses and common enterprise systems is helpful but not assumed.

Complete the [prerequisite setup](prerequisites/README.md) before beginning the
course.

## Lab Environment and Constraints

All course work must be completed on one macOS laptop using open-source tools
that can be installed with Homebrew.

* Live traffic exercises use the laptop's loopback interface (`lo0`) or an
  explicitly selected local interface.
* Multi-device behaviors are represented by the checksum-verified packet
  captures, route tables, logs, and diagrams in `labs/fixtures/`.
* All course fixtures are stored locally; internet access is needed only to
  install prerequisites.
* Participant outputs use local Markdown, text, CSV, or JSON files; the source
  diagram is `labs/fixtures/architecture/enterprise.md`.
* No exercise requires a second host, virtual machine, container runtime, cloud
  account, proprietary analyzer, or access to enterprise infrastructure.
* No exercise requires changing the laptop's routing, firewall, or DNS
  configuration.
* Live capture may require administrator approval, but saved captures support
  the same analysis without elevated privileges.
* Traffic must not be captured from or directed at systems outside the
  participant's control.

The course analyzes VLANs, VRFs, dynamic routing, firewalls, WANs, cloud
networks, and OT networks from local evidence and models rather than attempting
to emulate those systems on macOS.

## Course Method

Each module follows the same reasoning loop:

1. Establish the intended behavior.
2. Trace the packet path and forwarding decisions.
3. Identify policy, state, trust, and failure boundaries.
4. Determine what evidence should exist and where it can be collected.
5. Separate what is observed from what is inferred.
6. Explain the conclusion in language that other disciplines can verify.

Participants repeatedly produce three practical artifacts: a packet-path trace,
an annotated architecture diagram, and an evidence-backed incident narrative.

Detailed readings and exercises are available in the
[course module directory](modules/README.md).

All exercises use the checksum-verified [local lab dataset](labs/README.md).

## Module 1 — Operational Networking

> **Theme:** How packets actually get from A to B.

### Section 1 — Introduction and Mental Model

* Course objectives
* Network engineering vs. protocol implementation
* Control plane, data plane, and management plane
* Frames, packets, flows, and sessions
* Path, policy, state, and evidence
* The central question: What happens to this packet next, and how would we know?

### Section 2 — Layer 2 Networking

* Ethernet review
* MAC addresses
* MAC address tables and learning
* Broadcast domains
* ARP
* VLANs
* Access ports
* 802.1Q trunks
* Inter-VLAN communication
* Spanning Tree Protocol (STP/RSTP)
* Link aggregation and LACP

**Exercise:** Use `labs/fixtures/architecture/enterprise.md`,
`labs/fixtures/pcaps/foundations.pcap`, and
`labs/fixtures/routing/vrfs.json` to trace traffic within VLAN 10 and from VLAN
10 to the application segment.

**Output:** A hop-by-hop trace naming the frame, packet, address-resolution
step, and Layer 2 or Layer 3 decision at each boundary.

### Section 3 — Layer 3 and Packet Forwarding

* IPv4 addressing and CIDR
* IPv6 addressing at a conceptual level
* Subnets
* Default gateways
* ARP vs. IPv6 Neighbor Discovery
* Routing tables
* Longest-prefix matching
* Next-hop selection
* Default routes
* ECMP
* ICMP
* TTL and traceroute
* MTU
* Path MTU discovery
* TCP MSS
* NAT and PAT
* Asymmetric routing

**Exercise:** Use `labs/fixtures/routing/macos-routes.txt` and
`labs/fixtures/routing/route-candidates.csv` to determine the route for
`10.0.20.40` without changing the laptop's routes.

**Output:** The selected route, next hop, egress interface, and reason competing
routes were not selected.

### Section 4 — Transport, Naming, and Core Services

* TCP vs. UDP
* Ports, sockets, and client/server flows
* TCP connection establishment, state, teardown, and reset
* DNS resolution, delegation, caching, and failure modes
* DHCP address, gateway, and DNS assignment
* TLS session establishment and the visibility effects of encryption
* Dependencies between naming, transport, and application behavior

**Exercise:** Use `labs/fixtures/pcaps/foundations.pcap` to trace the DNS query,
TCP connection establishment, HTTP request and response, and connection
teardown. Identify every dependency and the frames that prove it.

**Output:** A dependency chain showing the traffic generated, the state created,
and the evidence available at each step.

### Section 5 — Dynamic Routing

#### OSPF

* Why dynamic routing exists
* Neighbors and adjacencies
* Link-state advertisements
* Link-state database
* SPF calculation
* Cost
* Areas
* Convergence
* ECMP
* Route redistribution

#### BGP

* Autonomous systems
* BGP peers
* eBGP vs. iBGP
* Prefix advertisement
* AS_PATH
* NEXT_HOP
* LOCAL_PREF
* Communities
* Route selection
* Route filtering

**Goal:** Understand routing conversations, not configure OSPF or BGP from
memory.

**Exercise:** Use `labs/fixtures/routing/ospf.json`,
`labs/fixtures/routing/bgp.json`, and `labs/fixtures/routing/route-events.jsonl`
to explain which route is selected, what changes after the modeled failure,
and what must converge.

### Section 6 — VRFs and Network Segmentation

* Virtual Routing and Forwarding (VRF)
* Multiple routing tables
* Route isolation
* Route leaking
* VRFs vs. VLANs
* Segmentation use cases

**Exercise:** Use `labs/fixtures/routing/vrfs.json` to explain why `CORP` has no
route to `10.0.30.50` while `OT` does, even though both routing contexts exist
on the same modeled router.

### Section 7 — Network Troubleshooting

Develop a systematic troubleshooting sequence:

1. Expected behavior, scope, and reproducibility
2. Physical connectivity
3. VLAN
4. ARP or IPv6 Neighbor Discovery
5. Local addressing
6. Gateway
7. Routing and VRF
8. ACL and policy
9. Firewall and session state
10. NAT
11. Return path
12. DNS
13. Application

For every test, state the hypothesis, change one variable, record the evidence,
and verify the return path.

#### Example Problems

* Host cannot reach its gateway.
* One subnet cannot reach another.
* A can initiate connections to B, but B cannot initiate connections to A.
* IP addresses work but hostnames do not.
* Small transfers work but large transfers fail.
* Traffic works through one path but not another.

**Exercise:** Diagnose the MTU failure represented by
`labs/fixtures/pcaps/mtu-failure.pcap`,
`labs/fixtures/routing/macos-routes.txt`, and
`labs/fixtures/incident/firewall.jsonl` without changing the laptop's network
settings.

### Section 8 — Module 1 Review

Participants should be able to answer:

> Given two endpoints and a network diagram, how does traffic get from A to B,
> and what devices and tables determine that path?

**Output:** A packet-path narrative that identifies forwarding decisions,
required state, policy checks, return-path assumptions, and two plausible
failure points.

## Module 2 — Network Architecture

> **Theme:** Why networks are designed the way they are.

Use `labs/fixtures/architecture/`, `labs/fixtures/routing/vrfs.json`, and
`labs/fixtures/network/l2-control.json` as the authoritative design evidence
for this module.

### Section 1 — Architecture Foundation Check

* Trace a representative flow across Layer 2 and Layer 3 boundaries
* Interpret the relevant forwarding and routing tables
* Identify required state, policy decisions, and return-path assumptions
* Record what the diagram or evidence does not establish

**Purpose:** Activate the packet-path model before evaluating architecture
decisions.

### Section 2 — Enterprise Network Architecture

* Access layer
* Distribution layer
* Core
* Collapsed core
* Layer 2 vs. Layer 3 boundaries
* Routed access
* First-hop redundancy
* HSRP and VRRP
* High-availability pairs
* Active/active vs. active/passive
* Failure domains
* Availability, scale, operability, and cost tradeoffs
* Redundancy vs. complexity

**Central questions:** What requirement does this design satisfy, and what
happens when this component fails?

### Section 3 — Network Boundaries and Services

* Network segmentation
* Security zones
* DMZs
* Management networks
* Out-of-band management
* OT zones, conduits, and industrial DMZs at a conceptual level
* Jump hosts and controlled remote access
* ACLs
* Stateful firewalls
* NAT
* Proxies
* Reverse proxies
* Load balancers
* IDS/IPS

For each component:

* What problem does it solve?
* Does it route traffic?
* Does it modify traffic?
* Does it enforce policy?
* Does it maintain state?
* Where does encryption begin or end?
* Does it produce useful telemetry?
* What dependencies and failure modes does it introduce?

### Section 4 — WAN and Remote Connectivity

* WAN concepts
* Multiple sites
* Internet connectivity
* Site-to-site VPNs
* IPsec
* Remote-access VPNs
* MPLS at a conceptual level
* SD-WAN at a conceptual level
* Redundant circuits
* Routing and failover

### Section 5 — Modern Data Center and Cloud Networking

Conceptual introduction to:

* Leaf/spine architectures
* East-west vs. north-south traffic
* Underlays
* Overlays
* VXLAN
* EVPN
* Cloud virtual networks, subnets, and route tables
* Security groups and network ACLs
* Transit gateways and hybrid connectivity

**Goal:** Understand why these technologies exist and recognize them in
architecture discussions.

### Section 6 — Reading a Network Architecture

Given an architecture diagram, identify:

* Layer 2 boundaries
* Layer 3 boundaries
* Routing points
* NAT
* Encryption
* Filtering
* Trust boundaries
* Security boundaries
* Failure domains
* Management boundaries
* Visibility boundaries
* Redundant paths
* Shared services and control-plane dependencies

For important traffic flows, ask:

* Where does this traffic originate?
* Where is it routed?
* Where is policy enforced?
* Where does encryption begin and end?
* Where could it be observed?
* What is the return path?
* What happens if a component or circuit fails?

**Output:** An annotated diagram and flow table showing path, policy, state,
trust, failure, management, and visibility boundaries.

### Section 7 — Architecture Tabletop

Analyze several failure scenarios:

* Access switch failure
* Distribution switch failure
* Firewall failure
* WAN circuit failure
* Routing-protocol failure
* Incorrect route advertisement
* Asymmetric routing
* Failed firewall state synchronization
* Shared-service or control-plane failure
* Cloud or hybrid-routing failure

**Output:** For each scenario, identify the affected flows, user-visible
symptom, available evidence, blast radius, and safest recovery action.

### Section 8 — Module 2 Review

Participants should be able to answer:

> Given an enterprise network diagram, what are its major design decisions,
> boundaries, dependencies, and failure modes?

**Output:** A concise architecture assessment that distinguishes confirmed
design facts from assumptions and unresolved questions.

## Module 3 — Incident Response and Integration

> **Theme:** Determine what actually happened on the network.

### Section 1 — Architecture-to-Evidence Bridge

* Select a critical traffic flow from an architecture diagram
* Predict its forward and return paths
* Identify the policy and state required at each boundary
* Predict which telemetry sources should observe the flow
* Identify visibility gaps before examining evidence

**Purpose:** Establish what should happen and what should be observable before
asking what actually happened.

### Section 2 — Network Security Telemetry

Compare the evidence provided by:

#### Packet Capture

* Full packets
* Payloads when traffic is not encrypted
* Timing
* Protocol behavior
* Dependence on capture location and completeness

#### NetFlow/IPFIX

* Source and destination
* Ports
* Protocol
* Duration
* Volume
* Sampling, aggregation, and exporter limitations

#### Infrastructure Logs

* DNS
* DHCP
* Firewalls
* Proxies
* VPNs
* Authentication

#### Network Security Monitoring

* Zeek
* IDS
* IPS
* Signature vs. behavioral detection

#### Endpoint and Aggregated Telemetry

* EDR
* SIEM

#### Evidence Quality

* Collection point and coverage
* Clock synchronization and time-zone normalization
* Sampling and aggregation
* Retention and data loss
* NAT, proxy, and load-balancer transformations
* Sensor health and collection gaps

For every telemetry source, ask:

1. What can it prove?
2. What can it suggest?
3. What can it not tell us?
4. Where must it be collected?
5. What visibility gaps remain?

**Output:** A telemetry matrix mapping each source to its collection point,
coverage, strengths, limitations, and retention assumptions.

**Exercise:** Process `labs/fixtures/pcaps/incident.pcap` with TShark and Zeek,
then compare frame-level facts with Zeek's `conn.log` and the records in
`labs/fixtures/incident/flows.jsonl`.

### Section 3 — Incident Response Concepts

* Event
* Alert
* Detection
* Incident
* Indicator of Compromise (IOC)
* Indicator of Attack (IOA)
* Tactics, Techniques, and Procedures (TTPs)
* MITRE ATT&CK
* Command and Control (C2)
* Beaconing
* Discovery
* Credential access
* Lateral movement
* Persistence
* Exfiltration
* Timeline construction
* Scoping and case definitions
* Alternative hypotheses and confidence levels
* Containment tradeoffs

#### Incident Lifecycle

1. Detection
2. Triage
3. Investigation
4. Scoping
5. Containment
6. Eradication
7. Recovery
8. Lessons learned

**Central question:** What evidence supports that conclusion?

**Output:** A preliminary timeline that labels each entry as observed, inferred,
hypothesized, or unknown.

### Section 4 — Investigation Exercise

#### Scenario

A user workstation is suspected of compromise.

#### Evidence Set

All evidence is stored under `labs/fixtures/` as local files:

* Architecture: `architecture/enterprise.md` and `routing/vrfs.json`
* Network: `pcaps/incident.pcap`, `incident/dns.jsonl`, and
  `incident/flows.jsonl`
* Controls: `incident/firewall.jsonl`, `incident/proxy.jsonl`, and
  `incident/vpn.jsonl`
* Host and identity: `incident/endpoint.jsonl` and `incident/auth.jsonl`
* Context and detection: `incident/assets.json` and `incident/siem.jsonl`

#### Possible Progression

```text
Workstation
    |
    v
DNS lookup
    |
    v
External C2
    |
    v
Internal discovery
    |
    v
Credential compromise
    |
    v
Lateral movement
    |
    v
Server access
    |
    v
Attempted access to protected network
```

For each step determine:

* What network traffic would be generated?
* What network path would it take?
* What security controls would it encounter?
* What telemetry might observe it?
* What evidence would remain?
* What alternative explanations are possible?
* What additional evidence would resolve uncertainty?

**Output:** An evidence ledger and incident narrative containing:

1. A normalized timeline
2. Confirmed observations and their sources
3. Competing hypotheses with confidence levels
4. Known visibility gaps
5. The next best evidence to collect
6. A defensible scope and containment recommendation

### Section 5 — Integrated Architecture and Incident Tabletop

Apply the investigation scenario to the enterprise/OT architecture in
`labs/fixtures/architecture/enterprise.md` and the route contexts in
`labs/fixtures/routing/vrfs.json`:

```text
Internet
   |
Edge Router
   |
Firewall
   |
   +------------------+
   |                  |
  DMZ             Enterprise
                      |
               Core/Distribution
                 /          \
              Users        Servers
                             |
                        OT Firewall
                             |
                           OT DMZ
                             |
                        OT Firewall
                             |
                     Supervisory LAN
                             |
                      Cell/Area Zones
                             |
                        PLC / IED
```

Analyze the same scenario from four perspectives.

#### Network Engineer

* How can packets get from source to destination?
* What routes are required?
* What VLANs and VRFs are involved?
* What happens during a failure?
* Could asymmetric routing occur?

#### Network Architect

* Why were these boundaries chosen?
* What are the trust boundaries?
* What are the failure domains?
* Where is redundancy required?
* What is the potential blast radius?

#### Security Engineer

* Where is policy enforced?
* Which communications should be permitted?
* What prevents lateral movement?
* Where should monitoring occur?

#### Incident Responder

* What actually happened?
* What evidence exists?
* What telemetry is missing?
* What is known versus inferred?
* How should the incident be scoped?
* What should be contained?

**Output:** A joint assessment that reconciles the four perspectives into one
packet path, boundary map, evidence summary, and prioritized action plan.

### Section 6 — Communication Exercise

Practice translating statements across disciplines using
`labs/fixtures/incident/flows.jsonl`,
`labs/fixtures/incident/firewall.jsonl`, and
`labs/fixtures/routing/vrfs.json`.

#### Example

> “NetFlow shows connections from the PLC VLAN to an external address, but the
> firewall team says the VRF has no default route.”

Work through:

* What is directly observed?
* What is inferred?
* What network conditions could make the observation possible?
* What configuration should be examined?
* What additional telemetry would resolve the discrepancy?

Practice asking high-value questions:

* “Which routing table is that prefix in?”
* “Where is the Layer 3 boundary?”
* “Is that traffic crossing VRFs?”
* “Where is policy actually enforced?”
* “Do we know the return path?”
* “Could this be asymmetric?”
* “What telemetry covers that segment?”
* “Is that conclusion based on PCAP, flow data, or logs?”
* “What evidence establishes lateral movement?”
* “Is the absence of evidence meaningful, or is this a visibility gap?”
* “Are we containing the incident or remediating the underlying problem?”

**Output:** A concise cross-functional handoff that states the observation,
impact, confidence, unknowns, requested action, and owner.

### Section 7 — Course Wrap-Up

#### Final Mental Model

```text
INTENDED BEHAVIOR
      |
      v
NETWORK ARCHITECTURE
      |
      v
ROUTING + SWITCHING + POLICY
      |
      v
   PACKET FLOW
      |
      v
   TELEMETRY
      |
      v
OBSERVED BEHAVIOR
      |
      v
INCIDENT RESPONSE
      |
      v
RECONSTRUCTED REALITY
```

#### Final Questions

For any network or incident, be able to ask:

1. What should happen?
2. How can the network make that happen?
3. Where is the relevant policy enforced?
4. What actually happened?
5. How do we know?
6. What don’t we know?
7. What failure, attack, or configuration could explain the difference?
8. What next action will reduce uncertainty or risk with the least disruption?

#### Completion Criteria

A participant can:

* Trace a representative flow in both directions.
* Explain the forwarding, policy, and state decisions along the path.
* Mark trust, failure, management, and visibility boundaries on an architecture
  diagram.
* Compare telemetry sources without overstating what they prove.
* Build an incident narrative that separates observations from inferences.
* Identify the most valuable next question, evidence source, or containment
  action.

The objective is not to become a network architect or incident responder. It is
to develop enough shared mental models and vocabulary to communicate effectively
with people who are.
