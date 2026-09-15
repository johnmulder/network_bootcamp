# Scenario and Evidence Set

> **Module 3 · Section 4**

## Why It Matters

The investigation begins with a suspected workstation compromise and a
deliberately incomplete set of local architecture, network, infrastructure,
endpoint, identity, and asset evidence.

## Core Model

* The initial suspicion is a lead, not a confirmed compromise.

* The architecture and route fixtures establish expected paths but may contain
  omissions or stale assumptions.

* The PCAP, flow, DNS, firewall, proxy, VPN, authentication, endpoint, and SIEM
  data have different scopes.

* Asset and identity context determine ownership, expected behavior, value, and
  response authority.

* Evidence must remain read-only; analysis outputs should be stored separately
  with source provenance.

## Reasoning Process

1. Inventory every source, time range, collection point, format, and integrity
   fact.

2. Read the case lead without allowing its wording to become the conclusion.

3. Build the expected path and visibility map before correlating observations.

4. Create an evidence ledger that preserves source references and analyst
   transformations.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict what asset identity and packet provenance
establish before assigning blame.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/assets.json
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
```

## Expected Evidence and Worked Reasoning

assets labels ws-23 and the server roles; packets supply observations, not
owner intent or complete history. A fixture digest protects these distributed
bytes, not original sensor completeness.

## Completion Standard

Inventory source, collection point or unknown, and scope without turning the
lead into a verdict.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which source is derived from another source in the set?

2. What important visibility is missing before analysis starts?

3. How will you prove a derived result came from a specific original file?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
