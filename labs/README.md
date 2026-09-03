# Local Lab Dataset

The course uses one fictional network and incident across all three modules.
Every address is private or reserved for documentation, and no exercise needs
traffic from an external system.

## Build and Verify

From the repository root:

```sh
python3 labs/build_fixtures.py
python3 labs/build_fixtures.py --check
```

The builder uses only the Python standard library. It creates deterministic
files under `labs/fixtures/` and records their SHA-256 digests in
`labs/fixtures/manifest.json`.

## Reference Endpoints

| Name | Address | Role |
| --- | --- | --- |
| `ws-23` | `10.0.10.23` | User workstation |
| `dns-1` | `10.0.10.53` | DNS resolver |
| `file-01` | `10.0.20.40` | Enterprise server |
| `historian-01` | `10.0.30.50` | OT DMZ historian |
| `supervisory-01` | `10.0.40.10` | Supervisory host |
| `external-77` | `198.51.100.77` | External documentation host |

## Fixture Groups

* `pcaps/` contains Ethernet, ARP, VLAN, DNS, TCP, HTTP, TLS, MTU, and incident
  traffic.
* `routing/` contains macOS-style routes plus VRF, OSPF, and BGP examples.
* `architecture/` contains the reference diagram, approved flows, cloud routes,
  and failure events.
* `incident/` contains DNS, flow, firewall, authentication, endpoint, proxy,
  VPN, SIEM, and asset evidence.

## Safety

Treat `labs/fixtures/` as read-only evidence. Write participant work under
`work/`. The builder can restore any changed fixture by regenerating the full
dataset.
