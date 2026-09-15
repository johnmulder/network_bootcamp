# IDS, IPS, and Monitoring Placement

> **Module 2 · Section 3**

## Why It Matters

Detection value depends as much on sensor placement and visibility as on
signatures or analytics. Inline prevention adds enforcement and availability
consequences.

## Core Model

* An IDS observes traffic and generates detections; an IPS is positioned to
  block or alter traffic inline.

* Signature detection matches known patterns, while behavioral methods identify
  deviations or suspicious sequences.

* Encryption, asymmetric paths, packet loss, encapsulation, and overloaded
  sensors reduce visibility.

* Sensor placement should correspond to important trust boundaries and
  investigation questions.

* An inline IPS can prevent traffic but also introduces latency, failure,
  tuning, and bypass considerations.

## Reasoning Process

1. Define the traffic and threat behavior that must be observed.

2. Choose a collection point that sees both directions and the useful stage of
   encryption.

3. Estimate capacity, packet loss, encapsulation, and evasion constraints.

4. Plan alert validation, failure behavior, tuning ownership, and evidence
   retention.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether placing an IDS before TLS termination
reveals application content.

Run from the repository root:

```sh
jq '.' labs/fixtures/architecture/components.json
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
```

## Expected Evidence and Worked Reasoning

The modeled IDS observes; ClientHello packets supply limited metadata.
Decryption or post-termination placement needs additional conditions.

## Completion Standard

Select a conceptual sensor location and name its visibility limit.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why can a well-tuned IDS miss traffic?

2. What new risk appears when detection becomes inline prevention?

3. Where should a sensor sit relative to TLS termination?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-41r1 §§2–4 — firewalls and policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final)

[Zeek — connection and protocol log reference](https://docs.zeek.org/en/current/reference/logs/index.html)
