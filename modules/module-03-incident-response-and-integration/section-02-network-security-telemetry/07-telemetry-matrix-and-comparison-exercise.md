# Telemetry Matrix and Comparison Exercise

> **Module 3 · Section 2**

## Why It Matters

The telemetry matrix forces every source to be evaluated by collection point,
strengths, limitations, retention, and evidentiary claim.

## Core Model

* Packet, flow, protocol, infrastructure, endpoint, and aggregated sources
  answer different questions.

* No source is universally strongest; usefulness depends on the claim being
  tested.

* Independent sources can corroborate a conclusion, while copied or derived
  sources are not independent.

* Conflicts can reveal clock, identity, path, transformation, or model errors.

* The matrix should identify the next best source when a claim exceeds current
  visibility.

## Reasoning Process

1. Process one saved PCAP with TShark and Zeek.

2. Correlate the results with named flow, infrastructure, endpoint, and SIEM
   events.

3. For each candidate claim, record which source proves, suggests, contradicts,
   or cannot address it.

4. Document conflicts and select the smallest additional evidence request.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which source best answers a packet-handshake
question and which answers process ancestry.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
jq '.' labs/fixtures/incident/siem.jsonl
```

## Expected Evidence and Worked Reasoning

Packets answer observed flags; endpoint source records answer recorded
ancestry. The SIEM inherits inputs. Optional Zeek can be run separately but is
not required to complete this comparison.

## Completion Standard

Build three claim/source rows and distinguish independence from format.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Did you mistake a derived Zeek log for independent corroboration of its
   source PCAP?

2. Which source best connects a network tuple to a process?

3. What additional source would resolve the most important conflict?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[Zeek — connection and protocol log reference](https://docs.zeek.org/en/current/reference/logs/index.html)

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
