
# Reference Architecture

Logical zone model; not a physical cable or interface inventory.
See [scenario and alias index](../../scenarios.md) before joining snapshots.

```text
Internet -- Edge role -- Enterprise firewall/NAT boundary
                            |
                CORP logical routing context
                |                         |
          Users VLAN 10              Servers VLAN 20
          ws-23 .10.23               app-01 / file-01 .20.40
          dns-1 .10.53

Separate controlled relationship (not server-as-router):
CORP -- OT firewall A boundary -- OT DMZ 30 historian .30.50
OT DMZ -- OT firewall B boundary -- Supervisory zone 40

MGMT VLAN 99: controlled management relationship to device/service roles.
Physical console links, power diversity, and actual traversal are unspecified.
```

CORP contains VLANs 10 and 20. OT contains VLANs 30 and 40. MGMT contains
VLAN 99. Intended flows are in traffic-flows.csv; routes are separate models.
Only app-01 is intended to initiate HTTPS to the historian in VLAN 30.
That service relationship is not a physical forwarding link through app-01.

Named functions with incomplete physical placement: core-acl (F1 policy
intention), jump-host-policy (F5), reverse proxy, load balancer, and IDS.
components.json supplies this model's capabilities; it does not supply
all backend tuples or wires. cloud-routes.json supplies attachment/table
relationships, not an Ethernet fabric. Management and return paths require
separate evidence. A boundary name alone is not proof of live enforcement.
