# Module 1 Workbench

This terminal workbench turns Module 1 fixture evidence into short, scored
challenges. It gives immediate feedback without modifying the fixtures or
requiring software beyond Python.

## Start Here

Run every command from the repository root.

List the activities:

```sh
python3 modules/module-01-operational-networking/workbench/module1_workbench.py list
```

Preview six worked questions before leading or attempting a session:

```sh
python3 modules/module-01-operational-networking/workbench/module1_workbench.py demo --seed 7 --limit 6
```

Practice one topic:

```sh
python3 modules/module-01-operational-networking/workbench/module1_workbench.py run routes --seed 7
```

Run a mixed review:

```sh
python3 modules/module-01-operational-networking/workbench/module1_workbench.py run all --seed 23 --limit 10
```

Verify the workbench and the fixtures it uses:

```sh
python3 modules/module-01-operational-networking/workbench/module1_workbench.py self-test
```

The seed controls only question order. Reusing a seed gives every learner the
same sequence and makes a group debrief reproducible.

## Activity Map

| Activity | Module 1 coverage | Primary evidence |
| --- | --- | --- |
| `l2` | Section 2: VLANs, STP, and LACP | `labs/fixtures/network/l2-control.json` |
| `routes` | Section 3: longest-prefix match and ECMP | `labs/fixtures/routing/route-candidates.csv` |
| `services` | Section 4: DHCP state and dependencies | `labs/fixtures/network/dhcp.jsonl` |
| `vrf` | Section 6: route isolation and route leaking | `labs/fixtures/routing/vrfs.json` |
| `troubleshooting` | Sections 7–8: evidence-driven diagnosis | `labs/fixtures/pcaps/` and `routing/traceroute.json` |

## Learning Routine

Use the same routine for individual practice or a facilitated group:

1. **Predict:** Answer before opening the cited fixture.
2. **Observe:** Read the exact evidence path printed with the question.
3. **Explain:** State the rule that connects the evidence to the answer.
4. **Challenge:** Name one plausible conclusion the evidence does not prove.
5. **Retry:** Reuse the seed after review, or change it for a new order.

The score measures exact answers. The explanation matters more: a learner
should be able to cite the prefix, field, frame, or record that made competing
answers lose.

## Evidence Commands

Use these commands when the workbench cites a fixture:

```sh
jq '.' labs/fixtures/network/l2-control.json
column -s, -t labs/fixtures/routing/route-candidates.csv
jq -c '.' labs/fixtures/network/dhcp.jsonl
jq '.' labs/fixtures/routing/vrfs.json
jq '.' labs/fixtures/routing/traceroute.json
tcpdump -nn -r labs/fixtures/pcaps/foundations.pcap
tcpdump -nn -r labs/fixtures/pcaps/mtu-failure.pcap
```

## Worked Examples

### Route Selection

Question: Which prefix wins for `10.0.20.99`?

1. The default route, `10.0.0.0/8`, and both `10.0.20.0/24` routes match.
2. `/24` is the longest matching prefix, so the default and `/8` lose before
   preference or metric is considered.
3. Both `/24` routes have the same source, preference, and metric.
4. The result is prefix `10.0.20.0/24` with two eligible ECMP next hops.

Observation: the CSV contains two equal selected rows. Interpretation: a
forwarder may hash different flows across their next hops; the table does not
prove which member a particular flow uses.

### VRF Reachability

Question: Does `OT` contain a route for `10.0.10.23`?

1. Examine only `.OT`; routes in `CORP` and `MGMT` are different contexts.
2. Neither `10.0.30.0/24` nor `10.0.40.0/24` matches `10.0.10.23`.
3. `OT` has no default route.
4. The answer is no, even though all three tables belong to the same modeled
   router.

This proves the route is absent from `OT`. It does not prove that no route leak,
firewall, or external forwarding path exists outside the fixture.

### MTU Troubleshooting

Question: TCP connects, a 1400-byte payload is sent, ICMP reports MTU 1200,
and the payload is retransmitted. What is the leading diagnosis?

1. Frames 1–3 complete the TCP handshake, so basic bidirectional reachability
   exists.
2. Frame 4 is the first 1400-byte payload.
3. Frame 5 reports that fragmentation is needed and names MTU 1200.
4. Frame 6 repeats the oversized payload.
5. The leading diagnosis is a path-MTU mismatch or failed Path MTU Discovery.

The evidence does not by itself identify which configuration should change.
That requires the complete path, endpoint behavior, and policy context.

## Facilitator Pattern

For a group, choose one seed and one activity. Ask learners to record an answer
and one-sentence justification before anyone opens the fixture. Run the same
activity in `demo` mode, then require the group to label each statement as
observation or interpretation.

Example:

```sh
python3 modules/module-01-operational-networking/workbench/module1_workbench.py demo troubleshooting --seed 12
```

Use `--limit 2` for a quick checkpoint and omit it for the complete activity.
The workbench reads only checksum-tracked fixtures and writes no learner data;
written analysis still belongs under `work/` as directed by each subsection.
