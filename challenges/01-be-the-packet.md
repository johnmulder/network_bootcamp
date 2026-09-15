<!-- delivery:start c01.brief -->
# Be the Packet

**Module 1 · 65 minutes · Deliverable: `work/bootcamp/packet-path.md`**

Your mission: explain how the workstation reaches its DNS resolver and an
application server. Start with [addresses and paths](reference.md#addresses-and-paths)
if IP addresses, prefixes, or MAC addresses are unfamiliar. No command syntax
needs to be memorized; run the commands below from the repository root.
<!-- delivery:end c01.brief -->

<!-- delivery:start c01.model -->
## Model One Hop — 10 Minutes

Use the first six minutes for the worked progression below and the last four
for a partner or solo prediction. This replaces the vocabulary-card tour.

1. `10.0.10.23` is an interface address. `/24` says the first 24 of 32 bits
   (three octets) identify its subnet: `10.0.10.0/24`.
2. `10.0.10.53` shares those three octets: deliver directly on this subnet.
   `10.0.20.40` differs: use the configured gateway for this example.
3. For remote delivery, put the server IP inside a frame addressed to the
   gateway MAC. ARP resolves that local neighbor; it does not change the
   packet destination into the gateway IP.
4. In an installed route table, a matching host route `/32` is more specific
   than its covering `/24` and default `/0`. We inspect that separate
   route-selection model later.

Worked conceptual row: host `192.0.2.10/24`, peer `192.0.2.20`, gateway
`192.0.2.1`; no unusual host routes or policy. The peer is local, so the
Ethernet destination is the peer MAC and the IP destination is `192.0.2.20`.
For a peer at `198.51.100.20`, use the gateway MAC with that remote peer IP.

| Header at the sending host | Local peer | Remote peer |
| --- | --- | --- |
| Outer Ethernet destination | Peer MAC | Gateway MAC |
| Inner IP destination | Peer IP | Remote peer IP |

Now predict the factory exchanges before reading their packet fields.

| Role | Address or function |
| --- | --- |
| Workstation `ws-23` | `10.0.10.23/24`, VLAN 10 |
| DNS resolver | `10.0.10.53`, same subnet |
| Gateway in the capture model | `10.0.10.1` |
| Application `app-01` / `file-01` | Two roles at `10.0.20.40` in this small model |
| Switch | Deliver within the VLAN using destination MAC and learned state |
| Router | Choose an IP next hop and construct the outgoing link-layer header |

Example: a host sending to a remote subnet first needs local delivery to an
appropriate router. The packet's IP destination remains the remote server.
Predict the destination MAC for the local DNS query and the remote application
request. Identify which missing neighbor information would require ARP.
<!-- delivery:end c01.model -->

<!-- delivery:start c01.inspect -->
## Inspect and Trace — 25 Minutes

```sh
jq '.' labs/fixtures/network/dhcp.jsonl
tshark -n -r labs/fixtures/pcaps/foundations.pcap
tshark -n -r labs/fixtures/pcaps/foundations.pcap -T fields -E header=y -e frame.number -e vlan.id -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.flags -e dns.qry.name -e http.response.code
```

Read a row left to right: `frame.number` is its citation, `eth.src/dst`
are link addresses, and `ip.src/dst` are packet addresses. `tcp.flags`
records bits such as SYN (`0x0002`), SYN+ACK (`0x0012`), and ACK (`0x0010`).
A blank field means that decoder supplied no value there: an ARP frame
has no `ip.src`, and a TCP row has no DNS name. Blank is not zero or proof
that a protocol never occurred elsewhere.

A JSON object has named fields: DHCP ACK `address` is a string, `prefix`
is a number, and `dns` is a list. JSONL stores one object per line; the
four lease lines are different messages in one transaction. Quote a field
and record, such as `network/dhcp.jsonl#4 gateway`, rather than a screen.

Use the packet sheet to record observations and cite frame numbers:

1. Find the assigned address, prefix, gateway, and resolver. Explain why DHCP
   configuration and a DNS answer solve different problems.
2. Compare the Ethernet destinations of the DNS query and the TCP SYN to the
   application. Which traffic stays on the local subnet?
3. Identify the DNS answer, TCP handshake, request, response, and beginning of
   connection closure. Does the capture show every packet needed for closure?
4. Trace the return packets at the observation point. Sketch the Ethernet
   headers expected on an unobserved downstream link, labeling assumptions.
5. Draw a service dependency chain. Which steps might use cached state? What
   would a UDP exchange omit? What would TLS prevent a passive observer from
   reading, and what would a ClientHello alone fail to prove?

Readable orientation: frame 1 is an ARP request, frame 3 a DNS query, and
frame 5 a TCP SYN. The modeled capture is on a VLAN 10 trunk. It does not
show the entire routed path or prove that the real network matches the diagram.
<!-- delivery:end c01.inspect -->

<!-- delivery:start c01.change -->
## Change One Condition — 20 Minutes

After your factual attempt, use the guided bounded routing experiment: predict
the effect of removing the host route, then compare the computed prefix and
eligible next hops. You can also compare the supplied CORP and OT contexts.
Use `experiment_predict` then `experiment_result` (terminal `x`, then `z`).
Record what changed and which policy or return-path facts remain unobserved.
Use this practice time for targeted support and reassessment if needed.

This CSV is an **independent route-selection snapshot**, not the table that
generated the earlier capture. Do not combine its next hops with the capture's
gateway and claim an observed path.

```sh
column -s, -t labs/fixtures/routing/route-candidates.csv
```

Choose the route for `10.0.20.40`. Now imagine only its `/32` route is removed.
Name the new winning prefix and every eligible next hop. Explain why a lower
preference number on a less-specific route does not win. What evidence would
identify the ECMP member actually used by one flow?

Use the reference card to contrast STP and LACP with this routed decision.
Neither redundant links nor an ECMP set imply that one flow uses all paths.
<!-- delivery:end c01.change -->

<!-- delivery:start c01.review -->
## Debrief and Checkpoint — 10 Minutes

Each learner explains one routing boundary, independently traces the important
return decision, and names one missing observation. Cite at least three useful
records across the sheet; do not paste entire command outputs.

Pass when another learner can distinguish your observed path from your modeled
header changes and explain your changed route choice. Use
[hints](hints.md#challenge-1) after an attempt and
[worked review](../facilitator/solutions.md#challenge-1) afterward.

Next: [The Transfer That Stops](02-the-transfer-that-stops.md).
<!-- delivery:end c01.review -->
