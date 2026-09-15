# Problem Patterns and Evidence-Bundle Exercise

> **Module 1 · Section 7**

## Why It Matters

Recurring symptom patterns are useful starting points, not diagnoses. This
exercise practices generating and eliminating multiple explanations from a
fixed evidence bundle.

## Core Model

* Gateway failure suggests local link, VLAN, address, neighbor, or
  gateway-interface problems.

* One-subnet failure suggests routing, VRF, policy, summarization, or
  return-path scope.

* One-way initiation suggests directional policy, stateful behavior, asymmetric
  routing, or application listening.

* Small-success and large-failure suggests MTU, MSS, fragmentation, buffering,
  or application limits.

* Path-dependent success suggests ECMP, aggregation members, inconsistent
  devices, or differing policy.

## Reasoning Process

1. List at least three hypotheses consistent with the symptom.

2. Identify the highest-information observation in the named fixture bundle.

3. Eliminate hypotheses only when evidence contradicts their predicted
   behavior.

4. State the leading explanation, confidence, remaining unknowns, and safest
   next test.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether every stalled transfer supports the
same MTU diagnosis.

Run from the repository root:

```sh
jq '.' labs/fixtures/network/troubleshooting.json
tshark -n -r labs/fixtures/pcaps/mtu-failure.pcap -Y 'tcp || icmp' -T fields -E header=y -e frame.number -e ip.len -e ip.hdr_len -e tcp.hdr_len -e tcp.len -e tcp.seq -e tcp.options.mss_val -e icmp.type -e icmp.code -e icmp.mtu
```

## Expected Evidence and Worked Reasoning

The MTU trace has size feedback; D1 has a naming timeout; L4 has
host-confirmed absence of a listener. A shared symptom does not imply a shared
cause.

## Completion Standard

Compare three mechanisms using one decisive observation each.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Did you treat the symptom pattern as a clue rather than proof?

2. Which hypothesis remains plausible because of a visibility gap?

3. What single additional artifact would most reduce uncertainty?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 1191 §3 — path MTU discovery](https://www.rfc-editor.org/rfc/rfc1191.html#section-3)

[RFC 9293 §3 — TCP operation](https://www.rfc-editor.org/rfc/rfc9293.html#section-3)
