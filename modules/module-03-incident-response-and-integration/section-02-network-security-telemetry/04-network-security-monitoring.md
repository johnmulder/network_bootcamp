# Network Security Monitoring: Zeek, IDS, and IPS

> **Module 3 · Section 2**

## Why It Matters

Network security monitoring transforms traffic into protocol records,
detections, and sometimes prevention. Derived telemetry accelerates analysis
but inherits sensor and analytic limitations.

## Core Model

* Zeek produces protocol-oriented logs and connection summaries from observed
  traffic rather than preserving every packet as the primary interface.

* An IDS alert indicates a rule or analytic matched observed data; it is not
  automatically an incident.

* An IPS can block inline, making its action part of both security evidence and
  service availability.

* Signature, anomaly, and behavioral detection have different coverage, tuning,
  and false-positive characteristics.

* Encrypted traffic, packet loss, asymmetric capture, evasion, and
  protocol-parser gaps affect all network monitoring.

## Reasoning Process

1. Identify the sensor, mode, policy, rule or script version, and traffic
   coverage.

2. Trace the alert back to supporting connection, protocol, and packet
   evidence.

3. Test benign and malicious alternative explanations.

4. Determine whether the sensor observed, inferred, or actively changed the
   traffic.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a SIEM alert or a Zeek parse supplies
an independent sensor observation.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/siem.jsonl
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
```

## Expected Evidence and Worked Reasoning

SIEM names flow and endpoint inputs; Zeek would parse the same incident PCAP.
Different output files do not create independent collection.

## Completion Standard

Trace one derived claim to its input; label rule/version gaps.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What does a Zeek connection state summarize?

2. Why is an IDS signature match not proof of compromise?

3. How does inline IPS placement change incident interpretation?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[Zeek — connection and protocol log reference](https://docs.zeek.org/en/current/reference/logs/index.html)

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
