# Spend Your Resilience Budget

**Module 2 · 60 minutes · Deliverable: `work/bootcamp/architecture.md`**

The factory can fund two improvements this quarter. Defend a design that
protects useful services, rather than counting redundant devices. Use the
packet-path sheet and [architecture vocabulary](reference.md#recognize-the-architecture-vocabulary).

## Understand the Requirement — 10 Minutes

These are fictional requirements for this tabletop, not facts proven by logs:

- Preserve the approved server-to-historian HTTPS service, while keeping
  direct user-to-historian HTTPS denied.
- Reduce disruption to established enterprise sessions during firewall
  failover and detect WAN impairment within one minute.
- Maintain an operational recovery path. Record which requirement your budget
  cannot fully satisfy and the evidence needed before implementation.

```sh
cat labs/fixtures/architecture/enterprise.md
jq '.' labs/fixtures/architecture/components.json
```

Compare the firewall, proxy, load balancer, and IDS: which routes, maintains
state, modifies traffic, enforces policy, or terminates TLS in this model?
Label routing, trust, management, failure, and visibility boundaries on your
diagram. A component's product category alone does not settle its behavior.

## Map Three Flows — 15 Minutes

```sh
column -s, -t labs/fixtures/architecture/traffic-flows.csv
jq '.' labs/fixtures/routing/vrfs.json
jq '.' labs/fixtures/architecture/cloud-routes.json
```

Compare F3 and F4. Identify the policy point and the different allowed source.
Mark missing route-leak, return-path, and live-rule evidence instead of treating
policy intent as proof of connectivity. For a cloud client `10.20.5.10` and
server `10.0.20.40`, look up forward and return routes in the cloud model.
What must be true beyond attachment and route presence?

## Spend, Then Handle a Failure — 20 Minutes

Each option costs one fictional token; spend two. These are exercise tradeoffs,
not real procurement prices or claims that a repair takes one unit of effort.

| Option | What it addresses | What it does not establish |
| --- | --- | --- |
| Validate and repair firewall state synchronization | Stale state on a standby device | Routing symmetry, application retry behavior, or complete failover success |
| Independently routed backup path | Loss of a transport path | Power independence, spare capacity, or application health |
| Service health monitoring | Detection of impairment beyond link-down | Automatic or successful recovery; polling/alert delay must be tested |
| Independent management access | Ability to diagnose and recover during an outage | That power and transport are actually independent |

Record your choices before reading the following failure evidence:

```sh
jq '.' labs/fixtures/architecture/wan.json
jq -c '.' labs/fixtures/architecture/failures.jsonl
```

Predict affected flows first; only then compare with the `affected` fields.
Distinguish existing NAT sessions from new connections during stale state
synchronization. A preferred WAN circuit has loss; what comparable measurement
is missing for the backup? Does interface-up status meet the requirement?

Now apply this **hypothetical twist**: both transport paths use the same
building power feed; management currently uses the preferred circuit. Revise
one assumption. Do not rewrite the original fixture to hide the difference.

## Defend the Decision — 15 Minutes

Give a 90-second pitch; your partner asks which failure remains. Alone, write
the strongest objection before revising. Include owner, prerequisite, expected
effect, a test against the requirement, and rollback for a proposed change.

Pass when the diagram and decision distinguish intent, measured state,
assumptions, and unknowns. No pair of tokens solves every requirement; justify
residual risk instead of promising certainty. Use [hints](hints.md#challenge-4)
and [worked review](../facilitator/solutions.md#challenge-4) after the attempt.

Next: [Suspicious Is Not Proven](05-suspicious-is-not-proven.md).
