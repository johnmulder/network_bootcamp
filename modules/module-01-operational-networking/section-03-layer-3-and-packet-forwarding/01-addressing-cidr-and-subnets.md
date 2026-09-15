# IPv4 Addressing, CIDR, and Subnets

> **Module 1 · Section 3**

## Why It Matters

Address and prefix interpretation determines whether a destination is local,
which route can match it, and how designs divide broadcast and routing domains.

## Core Model

* An IPv4 address identifies an interface; the prefix length identifies the
  network portion used for on-link and routing decisions.

* CIDR expresses contiguous prefix bits and supports variable-size networks and
  route aggregation.

* Network and broadcast addresses have special meaning in conventional IPv4
  subnets, while usable host ranges lie between them.

* Nested destination routes are normal: `10.0.20.40/32` overlaps its covering
  `10.0.20.0/24` and `10.0.0.0/8`. Longest-prefix matching selects the most
  specific installed match. Conflicting address assignments are a separate
  design problem; overlapping routes do not make a table malformed.

* Address membership is a binary prefix comparison, not a visual comparison of
  decimal octets.

## Worked Boundaries — Optional Beyond /24

The required day assesses `/24` membership. For other prefixes, compare
network bits using the mask. For `192.0.2.126/25`, 25 bits are fixed:

| Last octet | Binary | With mask `10000000` |
| --- | --- | --- |
| 126 | `01111110` | `00000000` |
| 129 | `10000001` | `10000000` |

The addresses fall in different halves: `.0–.127` and `.128–.255`. Under
conventional broadcast-subnet assumptions, the first half has network `.0`,
broadcast `.127`, and host range `.1–.126`. `/31` point-to-point and `/32`
host routes need separate conventions; do not apply that host-range rule
universally.

For `172.16.1.254/23`, the mask is `255.255.254.0`: the third octet
`00000001 AND 11111110` becomes zero. Its range is `172.16.0.0` through
`172.16.1.255`, so `172.16.0.8` belongs. Contrast practice: does
`172.16.2.8` belong? No: its masked third octet is two.

## Reasoning Process

1. Convert the prefix length into a mask or reason directly in binary.

2. Calculate the network boundary and address range.

3. Test whether source, destination, and gateway belong to the expected subnet.

4. Identify whether a host should use direct delivery or a gateway.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether 10.0.10.53 and 10.0.20.40 belong to
the DHCP client's /24.

Run from the repository root:

```sh
jq '.' labs/fixtures/network/dhcp.jsonl
```

## Expected Evidence and Worked Reasoning

ACK record 4 gives 10.0.10.23/24: the first three octets match only the
resolver. The worked /25 and /23 examples above are optional additional
methods.

## Completion Standard

Show the /24 comparison and one optional boundary calculation without a binary
leap.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why are `192.0.2.1/24` and `192.0.2.1/25` different forwarding statements?

2. How does route aggregation reduce routing-table size?

3. What happens when a configured gateway is outside the host's on-link prefix?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
