# IOCs, IOAs, TTPs, and MITRE ATT&CK

> **Module 3 · Section 3**

## Why It Matters

Indicators and behavior frameworks organize evidence at different levels. They
support investigation and communication but should not replace direct
reasoning.

## Core Model

* An Indicator of Compromise is an observable artifact associated with
  malicious activity, such as a hash, domain, address, file, or registry value.

* An Indicator of Attack emphasizes behavior or conditions suggesting an active
  technique.

* Tactics, techniques, and procedures describe goals, methods, and
  actor-specific implementation patterns.

* MITRE ATT&CK provides a shared knowledge base for adversary tactics and
  techniques, not a verdict or exhaustive detection checklist.

* Indicators can be reused, shared, stale, spoofed, or seen in benign contexts;
  behavior and context determine meaning.

## Reasoning Process

1. Identify the observable and its source, time, scope, and confidence.

2. Classify it as artifact, behavior, technique, or contextual relationship.

3. Map behavior to ATT&CK only after evidence supports the technique.

4. Use the mapping to find coverage and next questions, not to inflate
   certainty.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether a repeated external hostname is
itself proof of a C2 technique.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
```

## Expected Evidence and Worked Reasoning

ClientHello names and timing are observables. Benign update traffic can look
similar; ATT&CK terminology cannot supply missing command or compromise
evidence.

## Completion Standard

Classify the observable and state what would support a technique claim.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is an IP address rarely sufficient proof of compromise?

2. What does an ATT&CK technique mapping establish?

3. How does an IOA differ from a static IOC?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[MITRE ATT&CK — Command and Control tactic](https://attack.mitre.org/tactics/TA0011/)
