# Local Lab Dataset

The course uses one fictional network and incident across all three modules.
Every address is private or reserved for documentation, and no exercise needs
traffic from an external system.

The checked-in dataset contains 36 manifest-tracked evidence files plus
`labs/fixtures/manifest.json`. The builder creates every file deterministically
using only the Python standard library.

## Build and Verify

Run these commands from the repository root:

```sh
python3 labs/build_fixtures.py
python3 labs/build_fixtures.py --check
```

The first command regenerates the complete dataset. The second compares every
expected path and SHA-256 digest with the generated manifest without changing
the fixtures. A successful check reports `fixtures ready: 36 files`.

Treat `labs/fixtures/` as reproducible, read-only course evidence. Store notes,
derived output, diagrams, ledgers, and assessments under `work/`; rebuilding
fixtures does not modify that learner directory.

## Fixture Inventory

| Group | Files | Evidence represented |
| --- | ---: | --- |
| `architecture/` | 6 | Reference topology, component behavior, approved flows, cloud routes, WAN state, and failure events |
| `incident/` | 10 | Assets, DNS, flow, firewall, authentication, endpoint, proxy, VPN, SIEM, and the ledger template |
| `network/` | 3 | DHCP, IPv6, and Layer 2 control-plane state |
| `pcaps/` | 3 | Foundations, MTU failure, and incident packet captures |
| `routing/` | 7 | macOS routes, route candidates and events, traceroute, VRFs, OSPF, and BGP |
| `challenges/` | 7 | Neutral transfer capture, three staged incident rounds, two independent capstones, and provenance map |
| **Total evidence files** | **36** | All manifest-tracked fixtures, excluding the manifest itself |

The manifest is generated alongside those files and records each relative
path, byte length, and SHA-256 digest.

## Module Relationships

| Module | Primary fixture groups | Interactive use |
| --- | --- | --- |
| Module 1 | `network/`, `pcaps/`, and `routing/` | Layer 2, route, service, VRF, and troubleshooting decisions |
| Module 2 | `architecture/` | Flow, component, WAN, cloud, and failure-domain decisions |
| Module 3 | `incident/`, `pcaps/`, and architecture context | Telemetry, timeline, correlation, claim, and scope decisions |

The workbenches verify the exact fixture paths and checksums they consume:

```sh
python3 modules/module-01-operational-networking/workbench/module1_workbench.py self-test
python3 modules/module-02-network-architecture/workbench/module2_workbench.py self-test
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py self-test
```

## Reference Endpoints

| Name | Address | Role |
| --- | --- | --- |
| `ws-23` | `10.0.10.23` | User workstation |
| `dns-1` | `10.0.10.53` | DNS resolver |
| `file-01` | `10.0.20.40` | Enterprise server |
| `historian-01` | `10.0.30.50` | OT DMZ historian |
| `supervisory-01` | `10.0.40.10` | Supervisory host |
| `external-77` | `198.51.100.77` | External documentation host |

These stable identities allow the same path to be examined as forwarding
state in Module 1, architecture intent in Module 2, and correlated evidence in
Module 3.

## Incident Evidence Ledger

`incident/evidence-ledger-template.csv` defines the shared ten-field schema:

| Field | Purpose |
| --- | --- |
| `evidence_id` | Stable record identifier |
| `source` | File or sensor type |
| `collection_point` | Host, device, interface, or platform that observed it |
| `raw_time` | Timestamp exactly as recorded |
| `normalized_time` | Timestamp converted to the investigation standard |
| `entity` | Host, address, account, process, session, or rule |
| `observation` | Fact stated without causal interpretation |
| `classification` | Observed, inferred, hypothesized, or unknown |
| `limitation` | Coverage, derivation, clock, retention, or attribution gap |
| `confidence` | Claim-level confidence and its basis |

The [Module 3 workbench](../modules/module-03-incident-response-and-integration/workbench/README.md)
verifies this header and demonstrates how to normalize the 17-event timeline.

## Safety and Recovery

Saved fixtures are the default evidence path and require neither elevated
privileges nor network access. If a fixture is accidentally changed, regenerate
the complete dataset and then rerun `--check`. Do not put learner answers inside
`labs/fixtures/`, because regeneration replaces fixture content by design.

## One-Day Challenge Evidence

`challenges/transfer.pcap` is a byte-identical alias of the transfer-failure
capture. The three `incident-round-*.json` files preserve the original records
and filenames as keys, allowing gradual release without inventing new sensor
evidence. `challenges/evidence-map.json` maps aliases and rounds to their
original sources; the manifest covers both source and derived files.

`case-a.json` and `case-b.json` are separate, explicitly authored drills dated
the following day. Each provides complete route snapshots for its specified
flow, policy and state conditions, timestamped observations, and limitations.
They must not be joined to the original incident timeline. The capstone is
reviewed through the course rubric; there is no automatic diagnosis engine.
