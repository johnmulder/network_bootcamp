# Layer 2, Layer 3 Boundaries, and Routed Access

> **Module 2 · Section 2**

## Why It Matters

Boundary placement determines broadcast scope, convergence behavior, traffic
paths, and where policy or telemetry can be applied.

## Core Model

* Extending Layer 2 permits mobility and shared subnets but enlarges broadcast
  and spanning-tree failure domains.

* A Layer 3 boundary contains broadcasts and provides an explicit route and
  policy decision.

* Traditional access designs often route at distribution, while routed access
  places Layer 3 closer to access switches.

* First-hop gateway placement influences failure behavior and east-west paths.

* Boundary choice affects troubleshooting because it determines which tables
  and protocols decide forwarding.

## Reasoning Process

1. Mark every broadcast domain and default-gateway location.

2. Determine how far each VLAN extends and which links are routed.

3. Compare convergence and blast radius for a link, switch, or gateway failure.

4. Choose boundary placement based on endpoint, mobility, policy, and
   operational requirements.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether VLAN 10 extends physically through
the enterprise firewall.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number == 3 || frame.number == 5 || frame.number == 6' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e vlan.id -e tcp.flags
cat labs/fixtures/architecture/enterprise.md
```

## Expected Evidence and Worked Reasoning

The capture proves VLAN 10 at its trunk; the zone sketch gives logical
relationships. It does not provide a complete cable/port inventory.

## Completion Standard

Mark the known Layer 3 decision and leave physical VLAN extent unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What problem does routed access reduce?

2. Why might a design still extend Layer 2?

3. How does moving the gateway change an east-west packet path?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[IEEE 802.1Q — bridges and bridged networks](https://1.ieee802.org/maintenance/p802-1q-rev/)

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)
