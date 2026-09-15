# Optional Extensions

These activities are outside the six-hour course and do not affect completion.
Use existing deliverables for notes. Every network address below is local or
from the saved fixtures; no task sends traffic to enterprise or external hosts.

## Additional Saved Comparisons

- [Naming, attachment, and application failures](comparisons.md) — 25 minutes.
- [Capacity, goodput, RTT, loss, and receiver limits](comparisons.md#performance-is-more-than-link-speed--20-minutes)
  — 20 minutes.
- [Public DNS, TLS 1.3, and QUIC captures](../labs/exemplars/README.md) —
  10–15 minutes per card, with supplied test secrets clearly identified.
- [Recovery and closure](recovery.md) — ten minutes after both assessed cases.

## IPv6 Neighbor Detective — 15 Minutes

Prerequisite: distinguish local neighbors from routed destinations.

```sh
jq '.' labs/fixtures/network/ipv6.json
```

Predict how the host identifies its default router and how an interface scope
changes the meaning of a link-local address. Explain `REACHABLE` versus `STALE`
without treating STALE as proof that the neighbor is down. Identify which
router-advertisement fields are supplied and which actual packet exchanges
remain unobserved. Extend your packet sheet with one comparison to IPv4 ARP.

Review: `fe80::1%en0` is the default router. Scope selects the link; the
recorded `/64` prefix supports address configuration context. STALE means
reachability needs confirmation when used, not a recorded failure. The fixture
is a state snapshot, not a capture of Neighbor Discovery exchanges.

## The Cached Answer — 15 Minutes

Prerequisite: separate DNS answers from application reachability.

```sh
tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'dns.flags.response == 1' -T fields -E header=y -e frame.number -e dns.qry.name -e dns.a -e dns.resp.ttl
```

Hypothetical drill: the answer is cached at 15:00:00Z with its recorded TTL.
At 15:02:00Z an authoritative answer changes. Assuming no eviction, refresh,
or prefetch, may that cache still return the old answer? Calculate when its
entry expires. Distinguish this hypothetical from the original failure log.

Review: the A record has TTL 300 seconds, so under these stated assumptions
the old answer may remain until 15:05:00Z. An authoritative change does not
prove every cache has refreshed. Request the client's actual resolver/cache
view before diagnosing its current behavior.

## WAN Health Debate — 15 Minutes

Prerequisite: distinguish installed routes, policy, and application health.

```sh
jq '.' labs/fixtures/architecture/wan.json
```

Choose the next measurement for voice traffic under `lowest-loss`. Then state
this **new hypothetical observation**: VPN loss is 1%, measured with the same
probe method and interval as the private circuit's 20%. Does that alone settle
the choice for every application? Compare the branch default with the specific
HQ prefix, and consider capacity, latency, jitter, and actual failover policy.

Review: the added comparable loss measurement favors the VPN for a loss-based
choice, but does not establish sufficient capacity or low latency. The private
default and VPN-specific HQ route produce different paths. Record the new
measurement as an injected condition, not an original fixture fact.

## Local Socket Observation — 10 Minutes

Prerequisite: know the difference between a TCP connection and an application
response. This is an alternative observation during Challenge 1 or take-home
practice, not extra required class time. Use two terminals on the same Mac.

Terminal A, bind only to loopback:

```sh
nc -l 127.0.0.1 8765
```

Terminal B:

```sh
nc 127.0.0.1 8765
```

Type a short line and press Enter in each terminal. Explain why receiving that
line establishes more than a SYN alone but does not exercise a router, VLAN
trunk, or firewall failover. Press Control-C in both terminals when finished.
If the port is occupied, choose another unused local port in both commands.

No capture or administrator privilege is needed. If a live socket cannot be
opened, foundations frames 5–9 provide the equivalent saved comparison between
transport establishment and application data. Loopback does not model the
enterprise path; use the fixture for routing and policy conclusions.

## VXLAN and EVPN — Reference Only

Read the conceptual guide in Module 2 after understanding ordinary routing.
The repository does not supply VNI, VTEP mapping, or encapsulated-packet
evidence. A fabric lab would need those artifacts and a separate time budget;
the cloud route-table exercise cannot stand in for it.
