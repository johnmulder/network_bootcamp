# Module 2 Workbench

This terminal workbench turns the Module 2 architecture fixtures into short,
scored decisions. It checks answers immediately, cites the authoritative
fixture, and calls out missing evidence instead of silently filling gaps.

## Start Here

Run every command from the repository root.

For a guided five-question session, run `./course` and choose **Practice a
topic**. The commands below support repeatable or facilitated sessions.

List the activities:

```sh
python3 modules/module-02-network-architecture/workbench/module2_workbench.py list
```

Preview eight worked questions:

```sh
python3 modules/module-02-network-architecture/workbench/module2_workbench.py demo --seed 7 --limit 8
```

Practice one topic:

```sh
python3 modules/module-02-network-architecture/workbench/module2_workbench.py run cloud --seed 7
```

Run a mixed architecture review:

```sh
python3 modules/module-02-network-architecture/workbench/module2_workbench.py run all --seed 23 --limit 10
```

Verify the workbench and all fixtures it reads:

```sh
python3 modules/module-02-network-architecture/workbench/module2_workbench.py self-test
```

The seed controls question order. Reuse a seed for a shared group exercise or
change it to vary individual practice.

## Activity Map

| Activity | Module 2 coverage | Primary evidence |
| --- | --- | --- |
| `flows` | Sections 1, 3, and 6: path and policy boundaries | `architecture/traffic-flows.csv` |
| `components` | Sections 2–3: behavior and dependencies | `architecture/components.json` |
| `wan` | Section 4: transport, preference, and health | `architecture/wan.json` |
| `cloud` | Section 5: attachments and route selection | `architecture/cloud-routes.json` |
| `failures` | Sections 2 and 7–8: scope and blast radius | `architecture/failures.jsonl` |

All paths in the table are relative to `labs/fixtures/`.

## Architecture Routine

Use this loop for individual practice or a facilitated tabletop:

1. **Predict:** Choose the path, decision, behavior, or affected scope before
   opening the fixture.
2. **Trace:** Identify the exact route, policy point, capability, measurement,
   or failure record that controls the answer.
3. **Challenge:** State what the fixture does not establish and name the next
   evidence needed.
4. **Decide:** Give the safest conclusion or design action at the confidence
   supported by the evidence.
5. **Debrief:** Retry with the same seed and explain why every competing answer
   lost.

The score checks exact facts. A complete architecture answer also separates
observations from interpretations and includes return-path and failure-state
reasoning.

## Evidence Commands

Use these commands when the workbench cites a source:

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq 'to_entries[] | {component: .key, behavior: .value}' labs/fixtures/architecture/components.json
jq '.' labs/fixtures/architecture/wan.json
jq '.' labs/fixtures/architecture/cloud-routes.json
jq -c '.' labs/fixtures/architecture/failures.jsonl
```

## Claim Labels

| Label | Use it when | Example |
| --- | --- | --- |
| Confirmed | A fixture directly records the fact | `F4` is intended to be denied at `ot-firewall-a` |
| Interpretation | A rule is correctly applied to recorded facts | `/8` beats the default route |
| Assumption | The design expects a fact not present in evidence | The standby firewall has current state |
| Unknown | Required evidence is absent | Loss on `internet-vpn-1` |

Do not convert an unknown into a negative fact. An absent loss measurement does
not mean zero loss, and an attachment does not create a route that is absent
from its associated table.

## Worked Examples

### Flow and Policy Boundary

Compare `F3` and `F4` in `traffic-flows.csv`:

1. Both target `10.0.30.50` over TCP/443.
2. `F3` begins at `10.0.20.40` and is intended to be allowed.
3. `F4` begins at `10.0.10.23` and is intended to be denied.
4. The table assigns both intended decisions to `ot-firewall-a`.

Confirmed: the policy table distinguishes the two sources. Unknown: the table
does not prove that the live firewall currently has the intended rules or
state.

### Component Capability

Compare the enterprise firewall and reverse proxy:

1. Both enforce policy, modify traffic, and keep state.
2. The firewall routes traffic and records session, NAT, and deny telemetry.
3. The firewall does not terminate TLS in this model.
4. The reverse proxy terminates TLS and creates backend requests but does not
   route packets.

The label on a diagram is not enough. The capability fields determine whether
a component creates a new connection, changes an address, sees plaintext, or
becomes a stateful failure boundary.

### Cloud Forward and Return Routes

Trace a connection from `corp-vpc` to on-premises destination `10.0.20.40`:

1. `corp-vpc` uses `rt-corp`.
2. `10.0.20.40` matches `10.0.0.0/8`, whose target is `on-prem`.
3. For a return destination such as `10.20.5.10`, `on-prem` uses `rt-hybrid`.
4. `rt-hybrid` sends `10.20.0.0/16` to `corp-vpc`.

This supports a forward and return route for those prefixes. It does not prove
that distributed security controls, appliance state, or the physical hybrid
link permit the traffic.

### Partial WAN Failure

The WAN fixture records `private-1` as degraded with 20 percent loss. It records
`internet-vpn-1` as up and encrypted, but provides no loss measurement for it.

Therefore:

1. Link state alone is insufficient because the preferred private circuit is
   not down.
2. The `lowest-loss` voice policy cannot be evaluated from the fixture because
   one candidate lacks a comparable measurement.
3. The `private-preferred` business policy states intent, not whether degraded
   performance still satisfies the application requirement.
4. The next evidence should include comparable current loss, latency, and
   application-health measurements for both paths.

## Facilitator Pattern

Choose one seed and one activity. Require learners to record an answer, claim
label, and missing-evidence statement before revealing the result.

```sh
python3 modules/module-02-network-architecture/workbench/module2_workbench.py demo failures --seed 12
```

After the reveal, ask the group to trace normal, immediate-failure, converged,
and recovery states. Use `--limit 2` for a checkpoint or omit it for the full
activity.

The workbench reads checksum-tracked fixtures and writes nothing. Formal
architecture diagrams, flow tables, and assessments still belong under
`work/` as directed by each subsection guide.
