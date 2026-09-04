# Module 3 Workbench

This terminal workbench turns the Module 3 incident fixtures into a merged
timeline and short, scored investigation decisions. It checks answers
immediately, cites exact evidence, and separates what is observed from what is
only inferred or hypothesized.

## Start Here

Run every command from the repository root.

For a guided five-question session, run `./course` and choose **Practice a
topic**. The commands below support repeatable or facilitated sessions.

List the activities:

```sh
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py list
```

Build the normalized timeline:

```sh
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py timeline
```

Inspect one source in timeline order:

```sh
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py timeline --source endpoint
```

Preview eight worked questions:

```sh
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py demo --seed 7 --limit 8
```

Practice one investigation skill:

```sh
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py run claims --seed 7
```

Run a mixed review:

```sh
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py run all --seed 23 --limit 10
```

Verify the workbench, timeline, ledger schema, and evidence checksums:

```sh
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py self-test
```

The seed controls question order. Reuse it for a shared tabletop or change it
to vary individual practice.

## Activity Map

| Activity | Module 3 coverage | Primary evidence |
| --- | --- | --- |
| `telemetry` | Sections 1–2: strengths, gaps, and independence | Endpoint, flow, firewall, proxy, and SIEM logs |
| `timeline` | Sections 3–4: ordering and intervals | All incident JSONL sources |
| `correlation` | Sections 2–4: entities, processes, and sessions | DNS, endpoint, firewall, auth, and SIEM logs |
| `claims` | Sections 3–4 and 6: claim strength | Correlated incident evidence |
| `scope` | Sections 4–5 and 7: impact and unknowns | Asset, endpoint, flow, auth, and firewall evidence |

All source files are under `labs/fixtures/incident/`.

## Investigation Routine

Use this loop for individual practice or a facilitated investigation:

1. **Predict:** State what evidence should exist if the working hypothesis is
   true.
2. **Correlate:** Normalize time and join records through address, host,
   process, account, session, query, or rule.
3. **Classify:** Label each claim observed, inferred, hypothesized, or unknown.
4. **Challenge:** Write a plausible alternative and identify the evidence that
   would distinguish it.
5. **Act:** Choose the smallest reversible action that reduces risk while
   preserving evidence and essential operations.

The score checks exact facts and classifications. A complete investigation
also records source limitations, confidence, scope criteria, and rollback.

## Evidence Commands

Use these commands to inspect the workbench sources directly:

```sh
jq '.' labs/fixtures/incident/assets.json
jq -c '.' labs/fixtures/incident/dns.jsonl
jq -c '.' labs/fixtures/incident/flows.jsonl
jq -c '.' labs/fixtures/incident/firewall.jsonl
jq -c '.' labs/fixtures/incident/auth.jsonl
jq -c '.' labs/fixtures/incident/endpoint.jsonl
jq -c '.' labs/fixtures/incident/proxy.jsonl
jq -c '.' labs/fixtures/incident/vpn.jsonl
jq -c '.' labs/fixtures/incident/siem.jsonl
```

## Evidence-Ledger Schema

Use every field in the generated template:

| Field | Required content |
| --- | --- |
| `evidence_id` | Stable identifier such as `E-001` |
| `source` | File or sensor type |
| `collection_point` | Host, device, interface, or platform that observed it |
| `raw_time` | Timestamp exactly as recorded |
| `normalized_time` | Timestamp converted to the investigation standard |
| `entity` | Host, address, account, process, session, or rule |
| `observation` | Fact stated without causal interpretation |
| `classification` | Observed, inferred, hypothesized, or unknown |
| `limitation` | Coverage, derivation, clock, retention, or attribution gap |
| `confidence` | Claim-level confidence and its basis |

Display the exact header with:

```sh
head -n 1 labs/fixtures/incident/evidence-ledger-template.csv
```

## Worked Examples

### Timeline Correlation

The case sequence around `ws-23` is:

1. `15:59:58Z`: endpoint starts `update-agent`.
2. `16:00:00Z`: endpoint and DNS sources record the cdn-update query.
3. `16:01:00Z`: firewall, flow, and proxy sources record outbound TLS-related
   activity.
4. `16:02:00Z` and `16:03:00Z`: two more equal-size external flows begin.
5. `16:03:59Z`: endpoint starts child process `smb-client`.
6. `16:04:00Z`: the SMB flow to `file-01` begins.
7. `16:04:01Z`: `svc-backup` authentication succeeds on `file-01`.
8. `16:04:02Z`: the firewall records the SMB allow.
9. `16:04:10Z`: the SIEM alert is created.
10. `16:08:00Z`: direct user-to-OT HTTPS is denied.

Events sharing a timestamp are peers. The timeline sorts them for display, but
does not prove which occurred first or caused another.

### Independent and Derived Evidence

Zeek logs derived from `incident.pcap` are a second interpretation of the same
packets, not an independent observation. The SIEM alert explicitly names flow
and endpoint source events, so it is also derived.

Authentication, firewall, proxy, endpoint, and packet sensors can corroborate
one another only to the extent that their collection points and pipelines are
independent. Similar timestamps alone do not establish independence or cause.

### Claim Classification

| Claim | Classification | Reason |
| --- | --- | --- |
| DNS returned `198.51.100.77` | Observed | Exact DNS record |
| `update-agent` generated the TLS flows | Inferred | Timing and query align, but no process-to-socket record |
| The periodic TLS traffic is malicious C2 | Hypothesized | Periodicity has legitimate alternatives |
| Credentials were stolen | Unknown | Authentication success does not show acquisition |
| Direct user-to-OT access succeeded | Unsupported | The only direct record is a deny |

### Competing Explanations

Hypothesis A: `update-agent` is compromised and produces command-and-control
traffic followed by SMB discovery.

Hypothesis B: the agent is a legitimate updater using a temporary proxy bypass,
while the SMB process and scheduled service authentication are unrelated.

Evidence favoring A includes the new external destination, periodic flows, and
parent-child process timing. Evidence still needed includes process-to-socket
attribution, binary provenance, execution arguments, file activity, broader
endpoint prevalence, and external-destination reputation. The current fixture
does not eliminate B.

### Scope and Proportionate Containment

Confirmed scope includes `ws-23`, its external sessions, the SMB connection to
`file-01`, and successful `svc-backup` authentication. The evidence does not
prove successful OT access, persistence, credential theft, or exfiltration.

A proportionate initial action is to preserve volatile and endpoint evidence,
then restrict `ws-23` external and SMB communication through an existing
control. Record the owner, expected operational effect, validation signal, and
rollback. Do not isolate OT systems or disable shared accounts solely from this
fixture; collect the missing endpoint, identity, and service-owner evidence
first.

## Facilitator Pattern

Choose one seed and one activity. Before revealing answers, require each learner
to submit a claim label, exact evidence reference, alternative explanation, and
next-best evidence request.

```sh
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py demo correlation --seed 12
```

After the reveal, compare the merged timeline with each single-source view.
Use `--limit 2` for a checkpoint or omit it for the complete activity.

The workbench reads checksum-tracked fixtures and writes nothing. Formal
ledgers, narratives, scope statements, and handoffs still belong under `work/`
as directed by each subsection guide.
