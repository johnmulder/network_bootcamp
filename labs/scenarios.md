# Scenario and Observation Index

Choose the scenario before joining records. Reused addresses provide familiar
roles, not permission to merge independent snapshots into one observed path.
All factory records are constructed teaching evidence.

| Evidence | Scenario / time | Observation or model | What can be joined |
| --- | --- | --- | --- |
| `network/dhcp.jsonl`, `pcaps/foundations.pcap` | Foundations, August 15 at 14:59–15:00 UTC | Lease records and selected frames at a modeled VLAN 10 trunk; gateway `10.0.10.1` | Assigned settings and the healthy local trace, preserving limits on actual client state |
| `routing/macos-routes.txt` | Independent host-table snapshot | macOS-style installed routes; server subnet via `10.0.10.254` | Lookups inside this table; not the table used to construct foundations packets |
| `routing/route-candidates.csv` | Independent route-selection exercise | Candidate routes; server host route via `10.0.10.252`, covering `/24` via `.254` and `.253` | Before/after removal within this candidate model; not a captured gateway choice |
| `network/l2-control.json`, `network/ipv6.json` | Reference state models | STP/LACP/RA/neighbor fields, no captured control exchanges | Decisions supported by the fields; not unprovided partner state, exact timers, or actual ND messages |
| `routing/ospf.json`, `routing/route-events.jsonl` | R1 link-failure drill, 15:20 UTC | Next hops `10.255.0.2/.3`; timed control/forwarding events | Normal versus changed R1 state; no measured application recovery |
| `routing/bgp.json`, `routing/vrfs.json`, `routing/traceroute.json` | Separate reference exercises | Accepted advertisements, per-context routes, probe results | Only their declared policy/context/probe questions; no universal live route table |
| `pcaps/mtu-failure.pcap`, `challenges/transfer.pcap` | Transfer drill | Byte-identical captures at modeled VLAN 10 trunk | Same frames, two filenames; no extra independent source |
| `architecture/enterprise.md`, `components.json`, `traffic-flows.csv` | Reference design | Logical zones, modeled capabilities, intended flows | Intent and role comparisons; no physical port map or measured enforcement |
| `architecture/cloud-routes.json`, `wan.json` | Independent routing/transport models | Attachment targets and WAN attributes | Lookups and stated properties; not observed fabric links or full inspection state |
| `architecture/failures.jsonl` | Four separate failure drills | Power loss, stale sync, WAN loss, stale DNS at their listed times | One fault and its declared affected objects at a time; not simultaneous faults |
| `incident/*`, `pcaps/incident.pcap` | Original investigation, August 15 around 16:00 UTC | Endpoint/log sources plus modeled VLAN 10 packets; PCAP timing and source clocks have stated limits | Time/tuple correlation with source provenance; no missing process-to-socket attribution inferred |
| `challenges/incident-round-*.json` | Staged original incident | Copies grouped from the original log files | Preserve original filenames and record IDs; rounds add no new sensors |
| `challenges/case-a.json`, `case-b.json` | Independent drills on August 16 | Complete tables for specified flows and explicit policy/clock conditions | Each case internally; declared conditions override the incident's intentions for its test |
| `network/troubleshooting.json`, `architecture/performance.json` | Independent comparisons | Authored symptom snapshots and synthetic measurements | Compare only their declared methods and conditions |
| `challenges/recovery.json` | Hypothetical continuations, after both assessments | New changes, service observations, and owner decisions | Post-assessment closure practice; not evidence available in the original attempt |
| `labs/exemplars/*` | Independent upstream historical tests | Public captures with individual source notices, keys, and unknown tap placement where undocumented | Within each exemplar only; never correlate its addresses or clocks with the factory |

Paths in the first column are relative to `labs/fixtures/`, except the public
exemplars. The generated manifest records exact bytes; the exemplar manifest
separately records upstream provenance. A verified digest is a distribution
integrity check, not proof of original collection authenticity.

## Endpoint Inventory and Aliases

| Name | Address | Meaning in the reference model |
| --- | --- | --- |
| `ws-23` | `10.0.10.23` | User workstation, VLAN 10 / CORP |
| `dns-1` | `10.0.10.53` | Local resolver role |
| `app-01` / `file-01` | `10.0.20.40` | Two service roles at one address in this small model; the names do not establish two physical servers |
| `historian-01` | `10.0.30.50` | OT DMZ reporting role; not an assumed transit router |
| `supervisory-01` | `10.0.40.10` | Supervisory zone; direct PLC reachability is not demonstrated |
| `external-77` | `198.51.100.77` | Documentation endpoint; original incident and case B have different declared permissions |

Gateways belong to their snapshots: foundations `.1`, the host table's
server route `.254`, candidate server host route `.252`, and R1's next-hop
router IDs `10.255.0.2/.3`. These are not interchangeable observations.

## Physical Topology Versus Logical Relationships

The STP fixture explicitly supplies a three-switch link triangle; its diagram
can represent that modeled connectivity. The enterprise fixture is a logical
zone sketch. A complete physical cable, interface, power, and appliance map
is not supplied. Do not draw an invented wire merely to connect every icon.

For a service-flow overlay, state the source/destination, context, direction,
rule intention, and missing forwarding evidence. Management access needs its
own route and dependency review. `core-acl`, proxy, load balancer, and cloud
attachments are named functions with specified properties where provided;
their exact physical placement is unknown. Cloud route association is not
a leaf/spine topology. Use separate flow, topology, and dependency figures.

Legend for the course figures:

- Solid packet arrows: explicitly cited recorded frames.
- Dashed packet arrows: prediction or unobserved step, labeled in words.
- Topology edges: modeled links only when a topology source supplies them.
- Service/route/dependency/derivation edges: labeled with that relationship;
  they are not physical cabling.
- A zone or trust boundary groups roles; it does not prove enforcement.

For a complete worked packet diagram, use the Challenge 1 solution after an
attempt. The separate cloud and evidence-derivation figures answer different
questions; they should not be combined into a purported observed path.
