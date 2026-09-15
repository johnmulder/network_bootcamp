# NAT and PAT

> **Module 1 · Section 3**

## Why It Matters

Address and port translation changes observable identities across a boundary.
Investigations must track both sides of the mapping and the state that connects
them.

## Core Model

* Source NAT rewrites the source address, destination NAT rewrites the
  destination, and PAT also translates transport ports.

* A translation normally creates state keyed by protocol and endpoint tuples.

* Inside-local, inside-global, outside-local, and outside-global terminology
  describes viewpoints but varies across vendors.

* NAT does not inherently provide security; policy and stateful filtering are
  separate decisions even when implemented on one device.

* Logs must include mapping, timestamps, protocol, and ideally rule or device
  context to attribute translated traffic.

## Reasoning Process

1. Write the tuple before translation and the tuple after translation.

2. Identify which direction creates state and how return traffic matches it.

3. Mark where captures or logs observe each tuple.

4. Check expiry, port reuse, hairpin behavior, and asymmetric-path risks.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict how source translation changes attribution
for the external connection.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/firewall.jsonl
```

## Expected Evidence and Worked Reasoning

Firewall record 1 records source 10.0.10.23 translated to 192.0.2.44. Ports
and timing matter for PAT correlation; the log alone is not a complete
reverse-path capture.

## Completion Standard

Write the recorded address mapping and request the missing reverse
tuple/state.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is an external translated address insufficient to identify an internal
   host?

2. Can NAT occur without a firewall permit?

3. What evidence is required when translated ports are reused over time?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 3022 §2 — traditional NAT terminology](https://www.rfc-editor.org/rfc/rfc3022.html#section-2)

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)
