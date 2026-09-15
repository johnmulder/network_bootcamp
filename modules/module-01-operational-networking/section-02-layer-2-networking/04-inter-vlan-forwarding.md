# Inter-VLAN Forwarding

> **Module 1 · Section 2**

## Why It Matters

Traffic between VLANs requires a Layer 3 forwarding point. The transition
clarifies which addresses change and where routing or policy can be enforced.

## Core Model

* Hosts in different IP subnets send traffic to a default gateway rather than
  directly to the remote host's MAC address.

* The Layer 3 gateway can be a router interface, switch virtual interface,
  firewall interface, or another routed function.

* The gateway removes the incoming frame, performs a route lookup, applies
  relevant policy, and builds a new outgoing frame.

* The source and destination IP addresses usually remain unchanged, while
  source and destination MAC addresses change.

* Each routed direction can follow different devices, policies, or state, so
  the return path must be evaluated independently.

## Reasoning Process

1. Determine whether the destination is local or remote from the source host's
   perspective.

2. Resolve the source-side gateway MAC and describe the first frame.

3. At the gateway, perform the route and policy decisions for the destination
   subnet.

4. Construct the destination-side frame and repeat the analysis for the return
   path.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the first-hop MAC and downstream header for
the remote application.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/foundations.pcap -Y 'frame.number == 3 || frame.number == 5 || frame.number == 6' -T fields -E header=y -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e vlan.id -e tcp.flags
```

## Expected Evidence and Worked Reasoning

Frame 5 retains the server IP while targeting the gateway MAC. Frame 6 is the
reverse observation at the trunk. A downstream replacement header is a
prediction, not captured evidence.

## Completion Standard

Draw both directions; mark the downstream MAC values unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why does the source host not need the destination host's MAC address across
   VLANs?

2. Where can an ACL be applied during inter-VLAN forwarding?

3. What facts are needed to prove the return path uses the same gateway?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1812 §5.2.4.3 — forwarding selection](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3)

[RFC 826 — packet generation and reception](https://www.rfc-editor.org/rfc/rfc826.html)
