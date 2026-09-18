# Small Failure Comparisons

Use these independently authored snapshots after the foundations attempt.
They are not additional events in the factory incident. Keep notes in the
existing packet-path sheet. No live probes or new tools are required.

## Naming, Attachment, or Application? — 25 Minutes

Prerequisites: `/24`, next-hop versus endpoint, DNS, and a TShark row.
Spend five minutes predicting, ten inspecting, and ten explaining a next test.

```sh
jq '.' labs/fixtures/network/troubleshooting.json
```

| Record | Decisive saved observation | Bounded interpretation | Next discriminating check |
| --- | --- | --- | --- |
| D1 | No DNS reply at the client within three seconds | Timeout; no RCODE was observed | Did the resolver receive the query and send a reply? Compare both observation points |
| D2 | NXDOMAIN response | Resolver reports that queried name does not exist | Check queried name, resolver/view, and authoritative state; distinguish a typo or stale negative cache |
| D3 | NOERROR, empty AAAA answer, SOA, no referral | NODATA for the requested type; not name nonexistence | Query the needed type and inspect resolver/authority records |
| D4 | A answer, completed TCP, HTTP 503 | Naming and transport progress; application failure response | Correlate the request with service/backend logs |
| L1 | Link down and zero received frames in the interval | Local link failure is observed | Check cable, power, transceiver, and peer port; zero counters do not identify which |
| L2 | Link up, effective VLAN 20, expected VLAN 10 | The attachment does not match the declared design | Compare both port configurations and change history |
| L3 | Correct VLAN, ARP request, no reply; peer state absent | Neighbor resolution unresolved; exact cause unknown | Observe the request at the peer and its response/ownership state |
| L4 | Host receives SYN, emits RST; socket inventory has no listener | No TCP/443 listener in this bounded host snapshot | Verify intended service and its start/configuration logs |

RST alone would not prove no listener: filtering can also reject traffic.
L4 includes host evidence that narrows the conclusion. D1's lack of a reply
does not equal NXDOMAIN, and D3's empty answer is interpreted with its
response code, requested type, and authority context. An empty answer alone
could also be part of a referral or other response.

Contrast task: choose D2 versus D4 without looking at the interpretation
column. Name the next owner and evidence that would change your leading
explanation. Then compare L2 and L3: which supplied field separates them?
Complete when your answer cites a record, keeps unknowns explicit, and says
how two possible results of the next check lead to different actions.

## Before DHCP: Wireless and Access Authentication

A wired link-up or Wi-Fi association is only one attachment stage. An
enterprise port or wireless network may require 802.1X/EAP authentication;
the authenticator commonly consults RADIUS before authorizing data access
or assigning a VLAN. That exchange can fail before DHCP is possible.
Credentials, authentication outcome, assigned VLAN, and IP configuration
are different checks. These fixtures supply no wireless or RADIUS exchange.
Recognize the dependency; configuration and troubleshooting those systems
need a separate lab. See [RFC 3748 §1](https://www.rfc-editor.org/rfc/rfc3748.html)
and [RFC 3580 §3](https://www.rfc-editor.org/rfc/rfc3580.html).

## Performance Is More Than Link Speed — 20 Minutes

Prerequisites: bytes versus bits, a TCP stream, and route versus service
health. Spend five minutes calculating, ten comparing, and five choosing
the next check. The data are synthetic measurements with declared methods.

```sh
jq '.' labs/fixtures/architecture/performance.json
```

P1 receives 1,125,000,000 payload bytes in 60 seconds:
`bytes × 8 / seconds / 1,000,000 = 150 Mbps` goodput. Its link capacity is
200 Mbps. Protocol overhead, competing traffic, and endpoint constraints
mean these values need not be equal.

| Compare | What changes | What the next check should separate |
| --- | --- | --- |
| P1 → P2 | Same capacity and median RTT; less goodput, more probe loss and RTT variation | Inspect TCP retransmissions and congestion behavior versus receiver/competing-load limits; probe loss is not automatically TCP loss |
| P1 → P3 | Longer RTT and smaller receive window | `400,000 bytes × 8 / 0.080 seconds = 40 Mbps` is a receive-window/RTT bound for this simplified stream; inspect congestion window, window scaling, CPU and disk before assigning a unique cause |

The probe run sends 60 probes, one per second. P2 loses one: `1 / 60 × 100`
is 1.67% rounded to two decimal places. RTT is the median of received replies.
Here “jitter” is the mean absolute RTT difference between adjacent sent
probes only when both receive replies; pairs containing a loss are excluded.
It is RTT variation, not a measured one-way media jitter value.
Compare like methods, directions, payloads, intervals, and
warmup conditions. One measurement is not a service-level guarantee.

Backup exercise: 120 Mbps process reporting + 40 Mbps operations + 60 Mbps
bulk replication totals 220 Mbps of desired payload on a 200 Mbps link.
All of it cannot fit even before overhead. Pausing bulk leaves 160 Mbps;
that is a plausible budget, not proof of sufficient headroom. Ask the service
owner which demand can defer, then measure overhead and competing load.
Record a next check and an acceptance threshold for the critical service.

[RFC 6349 §§3–4](https://www.rfc-editor.org/rfc/rfc6349.html)
provides TCP measurement context. Sources reviewed September 14, 2026;
the exercises require no online access or iperf3 installation.
