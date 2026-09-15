# TLS Sessions and Encryption Visibility

> **Module 1 · Section 4**

## Why It Matters

TLS protects application data but leaves selected transport and handshake
metadata visible. Investigators must know where encryption begins and ends
before claiming what a sensor can prove.

## Core Model

* A TLS handshake negotiates protocol parameters and establishes traffic keys.
  Certificate-based handshakes authenticate with certificates; PSK-based
  handshakes, including resumption, can authenticate without a new certificate.

* Server Name Indication can expose the requested hostname in many TLS versions
  and configurations, while encrypted client hello can reduce that visibility.

* Certificates bind names to public keys through a trust chain and validity
  constraints; they do not prove the application is benign.

* After key establishment, payload content is encrypted, but addresses, ports,
  sizes, timing, and some handshake fields may remain observable.

* Proxies and load balancers can terminate and re-originate TLS, creating
  separate sessions and different observation points.

## Reasoning Process

1. In this TCP-based example, locate the connection and TLS messages. Secure
   application traffic can also use QUIC over UDP; TCP is not universal.

2. Separate ClientHello offers from ServerHello selections. Record certificate
   facts only if actually visible. TLS 1.3 encrypts most handshake content
   after ServerHello; supplied test secrets can change the analyst's view.

3. Mark each encryption termination point on the architecture.

4. State precisely what remains observable at every sensor location.

## Teaching Instructions

### Recognize QUIC

QUIC uses UDP and supplies its own connections, reliable streams, loss
recovery, congestion control, and TLS security. HTTP/3 uses QUIC. UDP's base
datagrams do not imply that the protocol built above them lacks reliability.
Port 443 alone distinguishes neither TCP/TLS from QUIC nor benign from
malicious use. Compare the
[public TLS and QUIC lesson cards](../../../labs/exemplars/README.md)
after the factory ClientHello exercise. Their public test secrets explain
visibility that an ordinary passive observer may lack.

[RFC 9000 §§2, 7](https://www.rfc-editor.org/rfc/rfc9000.html)
describes QUIC streams and connection establishment.

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which claims a ClientHello can establish
without a ServerHello or Finished.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
```

## Expected Evidence and Worked Reasoning

Frames 6, 10, and 14 offer TLS parameters. They do not establish negotiation,
certificates, Finished, or application success. Compare the separate public
TLS exemplar after this attempt.

## Completion Standard

Distinguish offered, selected, and encrypted/unobserved fields.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Does seeing a certificate prove which user initiated the connection?

2. Why can a proxy observe plaintext that a network tap cannot?

3. Which useful flow facts remain visible when payloads are encrypted?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 8446 §§2, 4 — TLS 1.3 handshake](https://www.rfc-editor.org/rfc/rfc8446.html)
