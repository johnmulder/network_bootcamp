# Local Lab Dataset

The core course uses a fictional factory and separately labeled snapshots.
Its generated addresses are private or reserved for documentation. The
[public exemplars](exemplars/README.md) are independent historical captures
and may contain real addresses. All exercises read local files offline.

Use the [scenario, observation, and alias index](scenarios.md) first. It
identifies each snapshot's gateway, collection point, and correlation limits.

The checked-in dataset contains 39 manifest-tracked evidence files plus
`labs/fixtures/manifest.json`. The builder creates those files deterministically
using only the Python standard library. Public captures have their own source
manifest, license notice, acquisition step, and checks under `labs/exemplars/`.

## Build and Verify

For routine verification, run this read-only command from the repository root:

```sh
python3 labs/build_fixtures.py --check
```

It checks file presence and SHA-256 digests against the existing manifest,
flags unlisted fixture files, parses JSON/JSONL, and checks the three original
PCAP magic headers. A successful check reports `fixtures ready: 39 files`.
It does not regenerate evidence or establish that an incident interpretation
is correct.

Maintainers can deliberately regenerate the dataset and manifest:

```sh
python3 labs/build_fixtures.py
```

Regeneration replaces generated evidence. Keep the builder and evidence from
the course copy that matches any saved sessions; changed fingerprints prevent
those sessions from resuming against a different copy.

Treat `labs/fixtures/` as reproducible, read-only course evidence. Store notes,
derived output, diagrams, ledgers, and assessments under `work/`; rebuilding
fixtures does not modify that learner directory.

## Fixture Inventory

| Group | Files | Evidence represented |
| --- | ---: | --- |
| `architecture/` | 7 | Logical topology, components, intended flows, cloud/WAN models, failure events, and performance comparisons |
| `incident/` | 10 | Assets, DNS, flow, firewall, authentication, endpoint, proxy, VPN, SIEM, and the ledger template |
| `network/` | 4 | DHCP, IPv6, Layer 2 state, and troubleshooting comparisons |
| `pcaps/` | 3 | Foundations, MTU failure, and incident packet captures |
| `routing/` | 7 | macOS routes, route candidates and events, traceroute, VRFs, OSPF, and BGP |
| `challenges/` | 8 | Neutral transfer capture, three incident rounds, two capstones, provenance map, and separate recovery epilogues |
| **Total evidence files** | **39** | All manifest-tracked fixtures, excluding the manifest itself |

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

`app-01` and `file-01` are two service roles at the same address. See the
[inventory](scenarios.md#endpoint-inventory-and-aliases) for alias and gateway
scope. Stable names help comparisons; they do not merge independent snapshots.

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
privileges nor network access. If a fixture is accidentally changed, restore
it and its manifest from the matching course copy, then rerun `--check`.
Regeneration is a deliberate maintainer operation, not an automatic session
recovery step. Do not put learner answers inside `labs/fixtures/`, because
regeneration replaces fixture content by design.

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
