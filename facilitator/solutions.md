# Worked Review and Evidence Map

Reveal only after the relevant attempt. These are defensible examples, not
required wording. Use the [rubric](README.md#assessment) to evaluate the
reasoning and accept other well-supported actions.

<!-- delivery:start opening.solution -->
## Opening Diagnostic

`10.0.10.23/24` and `10.0.10.53` are in the same IPv4 subnet. DNS success
establishes a returned answer, not server reachability. SYN/SYN-ACK/ACK
supports transport establishment at the observation point; it does not prove
TLS, a healthy application, or successful large transfers.
<!-- delivery:end opening.solution -->

<!-- delivery:start c01.solution -->
## Challenge 1

- DHCP OFFER/ACK supply `.23/24`, gateway `.1`, and resolver `.53`. They do
  not show whether those values remained installed at every later moment.
- Foundations frames 1–2 resolve the gateway's MAC. Frame 3 goes directly to
  DNS MAC `02:00:00:00:10:53`; frame 5 uses gateway MAC
  `02:00:00:00:10:01` while retaining IP destination `10.0.20.40`.
- Frame 4 answers the DNS query. Frames 5–7 establish TCP; frames 8–9 carry
  GET `/health` and HTTP 200. Frames 10–11 begin orderly closure, but the
  final acknowledgment of the client's FIN is not captured. Do not claim a
  fully observed teardown. DNS neighbor resolution may have used prior state;
  this capture does not supply its ARP exchange.
- Every captured frame carries VLAN 10. The downstream VLAN 20 headers are
  predictions, not captured facts. The synthetic capture does not measure
  every hop's TTL decrement or show all forwarding tables.
- In the **separate CSV exercise**, `.40/32` wins via `.252`. Removing that
  entry leaves two equal `/24` choices via `.254` and `.253`. Neither the
  default's preference nor the `/8` metric overrides specificity. Which ECMP
  member a particular flow uses remains unobserved.

Common misconception: copying the CSV's next hop into the PCAP explanation.
These are deliberately different instructional snapshots; require source
labels, not a fabricated combined topology.
<!-- delivery:end c01.solution -->

<!-- delivery:start c02.solution -->
## Challenge 2

The capture supports a path-size problem and incomplete effective PMTU
adaptation. Frame 4 carries 1400 TCP bytes inside a 1440-byte IPv4 packet.
Frame 5 quotes it in an ICMP fragmentation-needed error advertising MTU 1200.
Frame 6 repeats the original data after one second.

With fixed 20-byte IPv4 and TCP headers and no options or encapsulation,
`1200 - 20 - 20 = 1160` payload bytes fit. MSS 1460 is not proof that every
link supports that size. See [RFC 6691](https://www.rfc-editor.org/rfc/rfc6691.html)
for MSS and options, and [RFC 1191](https://www.rfc-editor.org/rfc/rfc1191.html)
for PMTU feedback.

The completed handshake weakens a hypothesis of total path failure. It does
not establish successful application or TLS exchange. ICMP is visible at the
modeled trunk, so “the capture proves ICMP was blocked” is wrong. Delivery to
the sender and its handling remain unknown. A synchronized host capture and
PMTU/transport state could distinguish those possibilities.

A good action asks the endpoint/network owner to check feedback delivery and
handling, then test appropriately sized data and application success. A
specific permanent configuration fix is not established by this fixture.
<!-- delivery:end c02.solution -->

<!-- delivery:start c03.solution -->
## Challenge 3

`route-events.jsonl` shows link-down at 0 ms, LSA at 50 ms, FIB installation at
80 ms, and flow rehash at 120 ms. The remaining installed next hop is
`10.255.0.3`. No application recovery timestamp or pre-detection outage period
is provided. Correlate packet loss, stateful-device behavior, and successful
application probes before reporting service recovery time.

In `bgp.json`, peer `192.0.2.2` has local preference 200, preferred over 100
despite its longer AS path in this example. The rejected advertisement does
not establish installed reachability. CORP has a default for the external
destination; OT does not. A route in one table does not become a route in the
other. Neither result alone settles policy and return-state questions.
<!-- delivery:end c03.solution -->

<!-- delivery:start c04.solution -->
## Challenge 4

F3 permits `10.0.20.40` to the historian over TCP/443; F4 denies the workstation
to that same service at `ot-firewall-a`. The diagram and route model do not
fully establish the inter-context forwarding implementation or live rules.
Mark those gaps. The cloud example selects `rt-corp`'s `10.0.0.0/8` toward
on-prem and `rt-hybrid`'s `10.20.0.0/16` for the return. Security controls and
appliance state still require verification.

The component fixture, not its label, establishes which modeled device routes,
terminates TLS, and produces telemetry. Both the reverse proxy and load
balancer terminate TLS here; the enterprise firewall does not.

An example two-token choice is firewall state repair plus service monitoring.
It addresses the stated session and detection requirements, provided failover
testing and alert latency validate them. It leaves transport recovery and
independent management underfunded. Backup path plus management is also
defensible if the learner explicitly accepts the unaddressed synchronization
and detection requirements and escalates that tradeoff.

`session-sync-stale` threatens established NAT sessions; it does not prove all
new sessions fail. The private WAN has 20% loss; the VPN lacks a comparable
loss measurement. “VPN up means zero loss” is unsupported. The shared-power
twist is an additional hypothetical condition, not an original recorded event.
Require dependency checks, a named owner, validation, rollback, and residual
risk. No token combination warrants a blanket availability guarantee.
<!-- delivery:end c04.solution -->

<!-- delivery:start c05.solution -->
## Challenge 5

Round 1 establishes an alert derived from flow and endpoint sources, three
equal-size external flow records at 60-second intervals, and an SMB flow.
These motivate investigation but do not establish C2 or a completed attack.

Round 2 ties `update-agent` directly to a DNS query and identifies `smb-client`
as its child. Authentication succeeds for `svc-backup` on `file-01` from the
workstation. The alternate `10:04:01-06:00` timestamp is `16:04:01Z`. It is
the same authentication record. There is no process-to-socket attribution,
credential-acquisition evidence, or proof of remote execution.

Round 3 records `TEMP-EGRESS-17` allowing external traffic and translation to
`192.0.2.44`, plus a proxy bypass. F2's intended deny differs from that observed
allow. A user-to-OT attempt is denied at `16:08:00Z`. The external flows start
in CORP, so OT's absent default route does not contradict them.

Example decisive ledger references:

| Original source / record | Observation | Limit |
| --- | --- | --- |
| `endpoint.jsonl` 1–2 | Agent starts, then queries the named domain | No socket attribution or binary provenance |
| `flows.jsonl` 1–3 | Repeated external tuple pattern | No payload or proof of motive |
| `firewall.jsonl` 1 | Allow rule, translated address, session `fw-9001` | One device's record; rule intent/approval not supplied |
| `endpoint.jsonl` 3 | Child `smb-client` starts | No proof of remote execution |
| `auth.jsonl` 2 | Successful network login on `file-01` | No proof of credential theft |
| `firewall.jsonl` 3 | Direct user-to-historian deny | Not proof that every OT path or asset is unaffected |
| `siem.jsonl` 1 | Alert names flow and endpoint dependencies | Derived evidence, not another independent sensor |

All listed source filenames are under `labs/fixtures/incident/`. Source type
alone does not prove independent collection pipelines. Record unknown sensor
health, retention, and incident clock precision rather than inventing values.

Two plausible hypotheses are compromised updater activity and a legitimate
updater using temporary egress alongside expected or unrelated SMB activity.
The current evidence does not eliminate the latter. Useful next evidence
includes process/socket attribution, binary provenance, file activity, broader
prevalence, and the temporary-rule approval record.

An example initial action is evidence preservation plus an owned review or
restriction of the workstation's external/SMB access, with service impact,
validation, and rollback documented. Do not infer a need to isolate OT systems
or disable a shared account from this evidence alone.
<!-- delivery:end c05.solution -->

## Challenge 6

<!-- delivery:start c06.case-a.solution -->
### Case A-v1

The forward `10.0.0.0/8` route still reaches on-prem. Before the change,
on-prem has `10.20.0.0/16` back toward the client; afterward it is absent and
there is no default in the complete flow-specific snapshot. A2 shows the
server receiving the SYN and emitting SYN-ACK; A3 records the return route
drop. A4 corroborates the client's timeout.

The supplied policy/state conditions do not support blaming the firewall.
The affected evidence concerns this cloud-to-server health flow, not all
factory services. The change's intent is unknown. Have network operations
check the change record and restore an authorized return route if unintended;
validate both TCP and TLS/application health, with rollback if the change
introduces new impairment. No post-repair success has been observed yet.
<!-- delivery:end c06.case-a.solution -->

<!-- delivery:start c06.case-b.solution -->
### Case B-v1

The ingress context changes from CORP to ISOLATED. CORP's default is irrelevant
to the active table, which has only the client-connected prefix and no leak.
B2 directly records a lookup miss. B3's absent firewall session alone would
not establish the cause, but the router record supplies it. The request fails
before reaching the firewall/NAT stage; this is not a recorded firewall deny.

The packet's source IP did not change; its routing context did. Do not borrow
the original incident's egress deny: the drill explicitly permits this test.
Check whether reassignment was intentional containment before returning it to
CORP. If unintended, coordinate the correction, validate the full service,
and preserve a rollback to the isolated state. Do not import a blanket default
into an isolation context just to make the probe work.
<!-- delivery:end c06.case-b.solution -->

## Provenance and Evidence Boundaries

`labs/fixtures/challenges/evidence-map.json` maps the neutral capture and three
round files to their sources. The parent manifest covers all 36 evidence
files; verify it before using derived selections. Round files are exact copies
of source records, not new sensor observations. Capstones A-v1 and B-v1 are
authored independent drills with explicit conditions and bounded clock
precision; do not transfer those conditions to the original incident.

Original architecture diagrams show intent and relationships; they do not
prove current policy, state, or all routing details. The foundation and incident
captures are modeled VLAN 10 observations. JSON route exercises use different
snapshots. Do not combine them into a purportedly measured end-to-end path.

Zeek logs derived from a capture share its observation boundary. The SIEM alert
explicitly depends on flow and endpoint events. Identical timestamps and
matching addresses can support correlation without establishing causation,
complete scope, sensor independence, or an unobserved attack step.
