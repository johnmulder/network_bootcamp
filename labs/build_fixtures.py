#!/usr/bin/env python3
"""Build the deterministic, local-only course fixtures."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def checksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    words = struct.unpack(f"!{len(data) // 2}H", data)
    total = sum(words)
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def mac(value: str) -> bytes:
    return bytes.fromhex(value.replace(":", ""))


def ip(value: str) -> bytes:
    return ipaddress.IPv4Address(value).packed


def ethernet(
    source: str,
    destination: str,
    ethertype: int,
    payload: bytes,
    vlan: int | None = None,
) -> bytes:
    header = mac(destination) + mac(source)
    if vlan is None:
        return header + struct.pack("!H", ethertype) + payload
    return header + struct.pack("!HHH", 0x8100, vlan, ethertype) + payload


def arp(
    operation: int,
    sender_mac: str,
    sender_ip: str,
    target_mac: str,
    target_ip: str,
) -> bytes:
    return struct.pack(
        "!HHBBH6s4s6s4s",
        1,
        0x0800,
        6,
        4,
        operation,
        mac(sender_mac),
        ip(sender_ip),
        mac(target_mac),
        ip(target_ip),
    )


def ipv4(
    source: str,
    destination: str,
    protocol: int,
    payload: bytes,
    identification: int,
    ttl: int = 64,
) -> bytes:
    first = 0x45
    total_length = 20 + len(payload)
    header = struct.pack(
        "!BBHHHBBH4s4s",
        first,
        0,
        total_length,
        identification,
        0x4000,
        ttl,
        protocol,
        0,
        ip(source),
        ip(destination),
    )
    header = header[:10] + struct.pack("!H", checksum(header)) + header[12:]
    return header + payload


def udp(
    source: str,
    destination: str,
    source_port: int,
    destination_port: int,
    payload: bytes,
) -> bytes:
    length = 8 + len(payload)
    header = struct.pack("!HHHH", source_port, destination_port, length, 0)
    pseudo = ip(source) + ip(destination) + struct.pack("!BBH", 0, 17, length)
    value = checksum(pseudo + header + payload)
    return struct.pack("!HHHH", source_port, destination_port, length, value) + payload


def tcp(
    source: str,
    destination: str,
    source_port: int,
    destination_port: int,
    sequence: int,
    acknowledgment: int,
    flags: int,
    payload: bytes = b"",
    options: bytes = b"",
) -> bytes:
    if len(options) % 4:
        options += b"\x01" * (4 - len(options) % 4)
    offset = (20 + len(options)) // 4
    header = struct.pack(
        "!HHIIBBHHH",
        source_port,
        destination_port,
        sequence,
        acknowledgment,
        offset << 4,
        flags,
        65535,
        0,
        0,
    ) + options
    length = len(header) + len(payload)
    pseudo = ip(source) + ip(destination) + struct.pack("!BBH", 0, 6, length)
    value = checksum(pseudo + header + payload)
    return header[:16] + struct.pack("!H", value) + header[18:] + payload


def dns_name(name: str) -> bytes:
    return b"".join(bytes([len(part)]) + part.encode() for part in name.split(".")) + b"\x00"


def dns_query(identifier: int, name: str) -> bytes:
    header = struct.pack("!HHHHHH", identifier, 0x0100, 1, 0, 0, 0)
    return header + dns_name(name) + struct.pack("!HH", 1, 1)


def dns_response(identifier: int, name: str, address: str) -> bytes:
    header = struct.pack("!HHHHHH", identifier, 0x8180, 1, 1, 0, 0)
    question = dns_name(name) + struct.pack("!HH", 1, 1)
    answer = struct.pack("!HHHLH4s", 0xC00C, 1, 1, 300, 4, ip(address))
    return header + question + answer


def tls_client_hello(name: str) -> bytes:
    server_name = name.encode()
    name_entry = b"\x00" + struct.pack("!H", len(server_name)) + server_name
    sni_body = struct.pack("!H", len(name_entry)) + name_entry
    sni = struct.pack("!HH", 0, len(sni_body)) + sni_body
    versions_body = b"\x02\x03\x04"
    versions = struct.pack("!HH", 43, len(versions_body)) + versions_body
    extensions = sni + versions
    random = bytes(range(32))
    body = (
        b"\x03\x03"
        + random
        + b"\x00"
        + struct.pack("!H", 2)
        + b"\x13\x01"
        + b"\x01\x00"
        + struct.pack("!H", len(extensions))
        + extensions
    )
    handshake = b"\x01" + len(body).to_bytes(3, "big") + body
    return b"\x16\x03\x01" + struct.pack("!H", len(handshake)) + handshake


def icmp_fragmentation_needed(original: bytes, mtu: int) -> bytes:
    body = struct.pack("!BBHHH", 3, 4, 0, 0, mtu) + original[:28]
    return body[:2] + struct.pack("!H", checksum(body)) + body[4:]


class Capture:
    def __init__(self) -> None:
        self.frames: list[tuple[float, bytes]] = []

    def add(self, timestamp: float, frame: bytes) -> None:
        self.frames.append((timestamp, frame))

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as handle:
            handle.write(struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
            for timestamp, frame in self.frames:
                seconds = int(timestamp)
                micros = int(round((timestamp - seconds) * 1_000_000))
                handle.write(struct.pack("<IIII", seconds, micros, len(frame), len(frame)))
                handle.write(frame)


def ip_frame(
    source_mac: str,
    destination_mac: str,
    source_ip: str,
    destination_ip: str,
    protocol: int,
    payload: bytes,
    identification: int,
    vlan: int | None = None,
    ttl: int = 64,
) -> bytes:
    packet = ipv4(source_ip, destination_ip, protocol, payload, identification, ttl)
    return ethernet(source_mac, destination_mac, 0x0800, packet, vlan)


def build_foundations() -> None:
    base = datetime(2026, 8, 15, 15, 0, tzinfo=timezone.utc).timestamp()
    client_mac = "02:00:00:00:10:23"
    gateway_mac = "02:00:00:00:10:01"
    dns_mac = "02:00:00:00:10:53"
    client = "10.0.10.23"
    gateway = "10.0.10.1"
    dns = "10.0.10.53"
    server = "10.0.20.40"
    capture = Capture()
    capture.add(
        base,
        ethernet(
            client_mac,
            "ff:ff:ff:ff:ff:ff",
            0x0806,
            arp(1, client_mac, client, "00:00:00:00:00:00", gateway),
            10,
        ),
    )
    capture.add(
        base + 0.010,
        ethernet(
            gateway_mac,
            client_mac,
            0x0806,
            arp(2, gateway_mac, gateway, client_mac, client),
            10,
        ),
    )
    query = dns_query(0x4242, "app.example.test")
    answer = dns_response(0x4242, "app.example.test", server)
    capture.add(base + 0.100, ip_frame(client_mac, dns_mac, client, dns, 17, udp(client, dns, 53000, 53, query), 1, 10))
    capture.add(base + 0.120, ip_frame(dns_mac, client_mac, dns, client, 17, udp(dns, client, 53, 53000, answer), 2, 10))
    client_seq = 1000
    server_seq = 9000
    mss = b"\x02\x04\x05\xb4"
    capture.add(base + 0.200, ip_frame(client_mac, gateway_mac, client, server, 6, tcp(client, server, 51514, 80, client_seq, 0, 0x02, options=mss), 3, 10))
    capture.add(base + 0.220, ip_frame(gateway_mac, client_mac, server, client, 6, tcp(server, client, 80, 51514, server_seq, client_seq + 1, 0x12, options=mss), 4, 10))
    capture.add(base + 0.230, ip_frame(client_mac, gateway_mac, client, server, 6, tcp(client, server, 51514, 80, client_seq + 1, server_seq + 1, 0x10), 5, 10))
    request = b"GET /health HTTP/1.1\r\nHost: app.example.test\r\nConnection: close\r\n\r\n"
    response = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nOK"
    capture.add(base + 0.240, ip_frame(client_mac, gateway_mac, client, server, 6, tcp(client, server, 51514, 80, client_seq + 1, server_seq + 1, 0x18, request), 6, 10))
    capture.add(base + 0.270, ip_frame(gateway_mac, client_mac, server, client, 6, tcp(server, client, 80, 51514, server_seq + 1, client_seq + 1 + len(request), 0x18, response), 7, 10))
    capture.add(base + 0.280, ip_frame(gateway_mac, client_mac, server, client, 6, tcp(server, client, 80, 51514, server_seq + 1 + len(response), client_seq + 1 + len(request), 0x11), 8, 10))
    capture.add(base + 0.290, ip_frame(client_mac, gateway_mac, client, server, 6, tcp(client, server, 51514, 80, client_seq + 1 + len(request), server_seq + 2 + len(response), 0x11), 9, 10))
    capture.write(FIXTURES / "pcaps" / "foundations.pcap")


def build_mtu_failure() -> None:
    base = datetime(2026, 8, 15, 15, 10, tzinfo=timezone.utc).timestamp()
    client_mac = "02:00:00:00:10:23"
    gateway_mac = "02:00:00:00:10:01"
    client = "10.0.10.23"
    gateway = "10.0.10.1"
    server = "203.0.113.20"
    capture = Capture()
    mss = b"\x02\x04\x05\xb4"
    syn_segment = tcp(client, server, 52000, 443, 100, 0, 0x02, options=mss)
    syn_packet = ipv4(client, server, 6, syn_segment, 100)
    capture.add(base, ethernet(client_mac, gateway_mac, 0x0800, syn_packet, 10))
    capture.add(base + 0.020, ip_frame(gateway_mac, client_mac, server, client, 6, tcp(server, client, 443, 52000, 500, 101, 0x12, options=mss), 101, 10))
    capture.add(base + 0.030, ip_frame(client_mac, gateway_mac, client, server, 6, tcp(client, server, 52000, 443, 101, 501, 0x10), 102, 10))
    payload = b"X" * 1400
    large = tcp(client, server, 52000, 443, 101, 501, 0x18, payload)
    large_packet = ipv4(client, server, 6, large, 103)
    capture.add(base + 0.040, ethernet(client_mac, gateway_mac, 0x0800, large_packet, 10))
    icmp = icmp_fragmentation_needed(large_packet, 1200)
    capture.add(base + 0.050, ip_frame(gateway_mac, client_mac, gateway, client, 1, icmp, 104, 10))
    capture.add(base + 1.040, ethernet(client_mac, gateway_mac, 0x0800, large_packet, 10))
    capture.write(FIXTURES / "pcaps" / "mtu-failure.pcap")


def build_incident() -> None:
    base = datetime(2026, 8, 15, 16, 0, tzinfo=timezone.utc).timestamp()
    client_mac = "02:00:00:00:10:23"
    gateway_mac = "02:00:00:00:10:01"
    dns_mac = "02:00:00:00:10:53"
    client = "10.0.10.23"
    dns = "10.0.10.53"
    c2 = "198.51.100.77"
    capture = Capture()
    query = dns_query(0x5151, "cdn-update.example.test")
    answer = dns_response(0x5151, "cdn-update.example.test", c2)
    capture.add(base, ip_frame(client_mac, dns_mac, client, dns, 17, udp(client, dns, 53100, 53, query), 200, 10))
    capture.add(base + 0.020, ip_frame(dns_mac, client_mac, dns, client, 17, udp(dns, client, 53, 53100, answer), 201, 10))
    hello = tls_client_hello("cdn-update.example.test")
    identification = 210
    for offset, source_port in ((60, 54000), (120, 54001), (180, 54002)):
        moment = base + offset
        cseq = 10000 + offset
        sseq = 20000 + offset
        capture.add(moment, ip_frame(client_mac, gateway_mac, client, c2, 6, tcp(client, c2, source_port, 443, cseq, 0, 0x02), identification, 10))
        capture.add(moment + 0.030, ip_frame(gateway_mac, client_mac, c2, client, 6, tcp(c2, client, 443, source_port, sseq, cseq + 1, 0x12), identification + 1, 10))
        capture.add(moment + 0.040, ip_frame(client_mac, gateway_mac, client, c2, 6, tcp(client, c2, source_port, 443, cseq + 1, sseq + 1, 0x10), identification + 2, 10))
        capture.add(moment + 0.050, ip_frame(client_mac, gateway_mac, client, c2, 6, tcp(client, c2, source_port, 443, cseq + 1, sseq + 1, 0x18, hello), identification + 3, 10))
        identification += 4
    for index, (target, port, accepted) in enumerate((
        ("10.0.20.40", 445, True),
        ("10.0.20.41", 445, False),
        ("10.0.20.42", 3389, False),
    )):
        moment = base + 240 + index
        source_port = 55000 + index
        cseq = 30000 + index
        capture.add(moment, ip_frame(client_mac, gateway_mac, client, target, 6, tcp(client, target, source_port, port, cseq, 0, 0x02), identification, 10))
        if accepted:
            capture.add(moment + 0.020, ip_frame(gateway_mac, client_mac, target, client, 6, tcp(target, client, port, source_port, 40000, cseq + 1, 0x12), identification + 1, 10))
        identification += 2
    capture.write(FIXTURES / "pcaps" / "incident.pcap")


def write_text(path: str, value: str) -> None:
    target = FIXTURES / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value.rstrip() + "\n")


def write_json(path: str, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True))


def write_jsonl(path: str, rows: list[dict[str, object]]) -> None:
    write_text(path, "\n".join(json.dumps(row, sort_keys=True) for row in rows))


def build_text_fixtures() -> None:
    write_json(
        "network/l2-control.json",
        {
            "vlans": {
                "10": {"name": "USERS", "subnet": "10.0.10.0/24"},
                "20": {"name": "SERVERS", "subnet": "10.0.20.0/24"},
            },
            "stp": {
                "root": "sw-dist-1",
                "bridges": [
                    {"name": "sw-dist-1", "priority": 24576, "mac": "02:00:00:00:00:01"},
                    {"name": "sw-access-1", "priority": 32768, "mac": "02:00:00:00:00:11"},
                    {"name": "sw-access-2", "priority": 32768, "mac": "02:00:00:00:00:12"},
                ],
                "links": [
                    {"a": "sw-dist-1", "b": "sw-access-1", "cost": 4, "state": "forwarding"},
                    {"a": "sw-dist-1", "b": "sw-access-2", "cost": 4, "state": "forwarding"},
                    {"a": "sw-access-1", "b": "sw-access-2", "cost": 4, "state": "discarding-on-access-2"},
                ],
            },
            "lacp": {
                "group": "ae1",
                "members": ["en1", "en2"],
                "minimum_links": 1,
                "flows": [
                    {"tuple": "10.0.10.23:51514-10.0.20.40:80-tcp", "member": "en1"},
                    {"tuple": "10.0.10.24:51515-10.0.20.40:80-tcp", "member": "en2"},
                    {"tuple": "10.0.10.25:51516-10.0.20.40:80-tcp", "member": "en1"},
                ],
            },
        },
    )
    write_json(
        "network/ipv6.json",
        {
            "host": "ws-23",
            "addresses": ["fe80::23%en0", "2001:db8:10::23/64"],
            "default_router": "fe80::1%en0",
            "neighbors": [
                {"address": "fe80::1%en0", "mac": "02:00:00:00:10:01", "state": "REACHABLE"},
                {"address": "2001:db8:10::53", "mac": "02:00:00:00:10:53", "state": "STALE"},
            ],
            "router_advertisement": {"prefix": "2001:db8:10::/64", "router_lifetime": 1800, "managed": False, "on_link": True, "autonomous": True, "valid_lifetime": 3600},
        },
    )
    write_jsonl(
        "network/dhcp.jsonl",
        [
            {"time": "2026-08-15T14:59:50Z", "message": "DISCOVER", "transaction": "0x1023", "client_mac": "02:00:00:00:10:23"},
            {"time": "2026-08-15T14:59:50.020Z", "message": "OFFER", "transaction": "0x1023", "address": "10.0.10.23", "prefix": 24, "gateway": "10.0.10.1", "dns": ["10.0.10.53"], "lease_seconds": 3600},
            {"time": "2026-08-15T14:59:50.040Z", "message": "REQUEST", "transaction": "0x1023", "address": "10.0.10.23"},
            {"time": "2026-08-15T14:59:50.060Z", "message": "ACK", "transaction": "0x1023", "address": "10.0.10.23", "prefix": 24, "gateway": "10.0.10.1", "dns": ["10.0.10.53"], "lease_seconds": 3600},
        ],
    )
    write_text(
        "routing/macos-routes.txt",
        """
Routing tables

Internet:
Destination        Gateway            Flags        Netif
default            10.0.10.1          UGScg          en0
10.0.10/24         link#14            UCS            en0
10.0.10.1/32       link#14            UCS            en0
10.0.20/24         10.0.10.254        UGSc           en0
10.0.30/24         10.0.10.253        UGSc           en0
127                127.0.0.1          UCS            lo0
198.51.100.77/32   10.0.10.252        UGSc           en0
""",
    )
    write_text(
        "routing/route-candidates.csv",
        """
prefix,source,preference,metric,next_hop,interface
0.0.0.0/0,static,1,0,10.0.10.1,en0
10.0.0.0/8,ospf,110,40,10.0.10.254,en0
10.0.20.0/24,ospf,110,20,10.0.10.254,en0
10.0.20.0/24,ospf,110,20,10.0.10.253,en0
10.0.20.40/32,static,1,0,10.0.10.252,en0
198.51.100.0/24,bgp,20,0,10.0.10.1,en0
198.51.100.77/32,static,1,0,10.0.10.252,en0
""",
    )
    write_json(
        "routing/vrfs.json",
        {
            "CORP": [
                {"prefix": "10.0.10.0/24", "next_hop": "connected"},
                {"prefix": "10.0.20.0/24", "next_hop": "10.0.10.254"},
                {"prefix": "0.0.0.0/0", "next_hop": "10.0.10.1"},
            ],
            "OT": [
                {"prefix": "10.0.30.0/24", "next_hop": "connected"},
                {"prefix": "10.0.40.0/24", "next_hop": "10.0.30.1"},
            ],
            "MGMT": [
                {"prefix": "10.0.99.0/24", "next_hop": "connected"},
                {"prefix": "10.0.10.0/24", "next_hop": "10.0.99.1"},
                {"prefix": "10.0.20.0/24", "next_hop": "10.0.99.1"},
            ],
        },
    )
    write_json(
        "routing/ospf.json",
        {
            "router": "R1",
            "neighbors": [
                {"id": "10.255.0.2", "state": "FULL", "cost": 10},
                {"id": "10.255.0.3", "state": "FULL", "cost": 10},
            ],
            "prefixes": [
                {"prefix": "10.0.20.0/24", "via": "10.255.0.2", "cost": 20},
                {"prefix": "10.0.20.0/24", "via": "10.255.0.3", "cost": 20},
                {"prefix": "10.0.30.0/24", "via": "10.255.0.3", "cost": 30},
            ],
        },
    )
    write_json(
        "routing/bgp.json",
        {
            "local_as": 64512,
            "routes": [
                {"prefix": "198.51.100.0/24", "peer": "192.0.2.1", "as_path": [64500], "local_pref": 100, "next_hop": "192.0.2.1", "accepted": True},
                {"prefix": "198.51.100.0/24", "peer": "192.0.2.2", "as_path": [64501, 64500], "local_pref": 200, "next_hop": "192.0.2.2", "accepted": True},
                {"prefix": "203.0.113.0/24", "peer": "192.0.2.3", "as_path": [64496], "local_pref": 100, "next_hop": "192.0.2.3", "accepted": False},
            ],
        },
    )
    write_json(
        "routing/traceroute.json",
        {
            "probe": {"source": "10.0.10.23", "destination": "203.0.113.20", "method": "udp", "first_ttl": 1},
            "hops": [
                {"ttl": 1, "response": "10.0.10.1", "rtt_ms": 0.8},
                {"ttl": 2, "response": "192.0.2.1", "rtt_ms": 5.1},
                {"ttl": 3, "response": None, "rtt_ms": None},
                {"ttl": 4, "response": "203.0.113.20", "rtt_ms": 18.4},
            ],
            "note": "TTL 3 forwarded the probe but did not return an ICMP response.",
        },
    )
    write_jsonl(
        "routing/route-events.jsonl",
        [
            {"time": "2026-08-15T15:20:00.000Z", "event": "link_down", "router": "R1", "neighbor": "10.255.0.2"},
            {"time": "2026-08-15T15:20:00.050Z", "event": "ospf_lsa", "router": "R1", "prefix": "10.0.20.0/24", "action": "withdraw-via-10.255.0.2"},
            {"time": "2026-08-15T15:20:00.080Z", "event": "fib_install", "router": "R1", "prefix": "10.0.20.0/24", "next_hop": "10.255.0.3"},
            {"time": "2026-08-15T15:20:00.120Z", "event": "flow_rehash", "router": "R1", "prefix": "10.0.20.0/24"},
        ],
    )
    write_text(
        "architecture/enterprise.md",
        """
# Reference Architecture

Logical zone model; not a physical cable or interface inventory.
See [scenario and alias index](../../scenarios.md) before joining snapshots.

```text
Internet -- Edge role -- Enterprise firewall/NAT boundary
                            |
                CORP logical routing context
                |                         |
          Users VLAN 10              Servers VLAN 20
          ws-23 .10.23               app-01 / file-01 .20.40
          dns-1 .10.53

Separate controlled relationship (not server-as-router):
CORP -- OT firewall A boundary -- OT DMZ 30 historian .30.50
OT DMZ -- OT firewall B boundary -- Supervisory zone 40

MGMT VLAN 99: controlled management relationship to device/service roles.
Physical console links, power diversity, and actual traversal are unspecified.
```

CORP contains VLANs 10 and 20. OT contains VLANs 30 and 40. MGMT contains
VLAN 99. Intended flows are in traffic-flows.csv; routes are separate models.
Only app-01 is intended to initiate HTTPS to the historian in VLAN 30.
That service relationship is not a physical forwarding link through app-01.

Named functions with incomplete physical placement: core-acl (F1 policy
intention), jump-host-policy (F5), reverse proxy, load balancer, and IDS.
components.json supplies this model's capabilities; it does not supply
all backend tuples or wires. cloud-routes.json supplies attachment/table
relationships, not an Ethernet fabric. Management and return paths require
separate evidence. A boundary name alone is not proof of live enforcement.
""",
    )
    write_text(
        "architecture/traffic-flows.csv",
        """
id,source,destination,protocol,port,intended,policy_point
F1,10.0.10.23,10.0.20.40,tcp,80,allow,core-acl
F2,10.0.10.23,198.51.100.77,tcp,443,deny,enterprise-firewall
F3,10.0.20.40,10.0.30.50,tcp,443,allow,ot-firewall-a
F4,10.0.10.23,10.0.30.50,tcp,443,deny,ot-firewall-a
F5,10.0.99.10,10.0.40.10,tcp,22,allow,jump-host-policy
""",
    )
    write_json(
        "architecture/cloud-routes.json",
        {
            "attachments": {
                "corp-vpc": "rt-corp",
                "security-vpc": "rt-security",
                "on-prem": "rt-hybrid",
            },
            "routes": {
                "rt-corp": [
                    {"prefix": "0.0.0.0/0", "target": "security-vpc"},
                    {"prefix": "10.0.0.0/8", "target": "on-prem"},
                ],
                "rt-security": [
                    {"prefix": "0.0.0.0/0", "target": "internet"},
                    {"prefix": "10.20.0.0/16", "target": "corp-vpc"},
                ],
                "rt-hybrid": [
                    {"prefix": "10.20.0.0/16", "target": "corp-vpc"},
                ],
            },
        },
    )
    write_json(
        "architecture/wan.json",
        {
            "sites": {
                "hq": {"prefix": "10.0.0.0/16", "internet_exit": True},
                "branch": {"prefix": "10.10.0.0/16", "internet_exit": False},
            },
            "circuits": [
                {"name": "private-1", "provider": "A", "capacity_mbps": 500, "preference": 10, "state": "degraded", "loss_percent": 20},
                {"name": "internet-vpn-1", "provider": "B", "capacity_mbps": 200, "preference": 20, "state": "up", "encrypted": True},
            ],
            "routes": [
                {"site": "branch", "prefix": "0.0.0.0/0", "next_hop": "hq", "circuit": "private-1"},
                {"site": "branch", "prefix": "10.0.0.0/16", "next_hop": "hq", "circuit": "internet-vpn-1"},
            ],
            "sdwan_policy": {"voice": "lowest-loss", "business": "private-preferred", "bulk": "lowest-cost"},
            "mpls": {"encrypted": False, "routing": "provider-managed-l3vpn"},
        },
    )
    write_json(
        "architecture/components.json",
        {
            "enterprise-firewall": {"routes": True, "modifies": True, "policy": True, "state": True, "tls_termination": False, "telemetry": ["sessions", "nat", "deny"]},
            "reverse-proxy": {"routes": False, "modifies": True, "policy": True, "state": True, "tls_termination": True, "telemetry": ["request", "response", "backend"]},
            "ids": {"routes": False, "modifies": False, "policy": False, "state": True, "tls_termination": False, "telemetry": ["alert", "protocol"]},
            "load-balancer": {"routes": True, "modifies": True, "policy": True, "state": True, "tls_termination": True, "telemetry": ["client", "backend", "health"]},
        },
    )
    write_jsonl(
        "architecture/failures.jsonl",
        [
            {"time": "2026-08-15T15:30:00Z", "component": "access-sw-1", "condition": "power-loss", "affected": ["ws-23"]},
            {"time": "2026-08-15T15:40:00Z", "component": "enterprise-fw-a", "condition": "session-sync-stale", "affected": ["established-nat-sessions"]},
            {"time": "2026-08-15T15:50:00Z", "component": "wan-1", "condition": "20-percent-loss", "affected": ["branch-applications"]},
            {"time": "2026-08-15T15:55:00Z", "component": "dns-1", "condition": "stale-answer", "affected": ["app.example.test"]},
        ],
    )
    write_json(
        "incident/assets.json",
        {
            "10.0.10.23": {"host": "ws-23", "owner": "alex", "role": "user-workstation"},
            "10.0.20.40": {"host": "file-01", "owner": "platform", "role": "file-server"},
            "10.0.20.41": {"host": "app-02", "owner": "platform", "role": "application"},
            "10.0.20.42": {"host": "admin-01", "owner": "it", "role": "admin-workstation"},
            "198.51.100.77": {"host": "external-77", "owner": "unknown", "role": "external"},
        },
    )
    write_jsonl(
        "incident/dns.jsonl",
        [
            {"time": "2026-08-15T16:00:00.000Z", "client": "10.0.10.23", "query": "cdn-update.example.test", "type": "A", "answer": "198.51.100.77", "rcode": "NOERROR"},
            {"time": "2026-08-15T16:10:00.000Z", "client": "10.0.20.40", "query": "historian.ot.example.test", "type": "A", "answer": "10.0.30.50", "rcode": "NOERROR"},
        ],
    )
    write_jsonl(
        "incident/flows.jsonl",
        [
            {"start": "2026-08-15T16:01:00Z", "end": "2026-08-15T16:01:01Z", "src": "10.0.10.23", "sport": 54000, "dst": "198.51.100.77", "dport": 443, "protocol": "tcp", "bytes": 278},
            {"start": "2026-08-15T16:02:00Z", "end": "2026-08-15T16:02:01Z", "src": "10.0.10.23", "sport": 54001, "dst": "198.51.100.77", "dport": 443, "protocol": "tcp", "bytes": 278},
            {"start": "2026-08-15T16:03:00Z", "end": "2026-08-15T16:03:01Z", "src": "10.0.10.23", "sport": 54002, "dst": "198.51.100.77", "dport": 443, "protocol": "tcp", "bytes": 278},
            {"start": "2026-08-15T16:04:00Z", "end": "2026-08-15T16:04:03Z", "src": "10.0.10.23", "sport": 55000, "dst": "10.0.20.40", "dport": 445, "protocol": "tcp", "bytes": 1198},
        ],
    )
    write_jsonl(
        "incident/firewall.jsonl",
        [
            {"time": "2026-08-15T16:01:00Z", "rule": "TEMP-EGRESS-17", "action": "allow", "src": "10.0.10.23", "translated_src": "192.0.2.44", "dst": "198.51.100.77", "dport": 443, "session": "fw-9001"},
            {"time": "2026-08-15T16:04:02Z", "rule": "USER-TO-SERVER", "action": "allow", "src": "10.0.10.23", "dst": "10.0.20.40", "dport": 445, "session": "fw-9010"},
            {"time": "2026-08-15T16:08:00Z", "rule": "DENY-USER-OT", "action": "deny", "src": "10.0.10.23", "dst": "10.0.30.50", "dport": 443, "session": None},
        ],
    )
    write_jsonl(
        "incident/auth.jsonl",
        [
            {"time": "2026-08-15T15:59:40Z", "host": "ws-23", "user": "alex", "result": "success", "method": "console"},
            {"time": "2026-08-15T16:04:01Z", "host": "file-01", "user": "svc-backup", "source": "10.0.10.23", "result": "success", "method": "network"},
        ],
    )
    write_jsonl(
        "incident/endpoint.jsonl",
        [
            {"time": "2026-08-15T15:59:58Z", "host": "ws-23", "event": "process_start", "process": "update-agent", "parent": "launchd", "sha256": "f" * 64},
            {"time": "2026-08-15T16:00:00Z", "host": "ws-23", "event": "dns_query", "process": "update-agent", "query": "cdn-update.example.test"},
            {"time": "2026-08-15T16:03:59Z", "host": "ws-23", "event": "process_start", "process": "smb-client", "parent": "update-agent", "user": "alex"},
        ],
    )
    write_jsonl(
        "incident/proxy.jsonl",
        [
            {"time": "2026-08-15T16:01:00Z", "client": "10.0.10.23", "method": "CONNECT", "host": "cdn-update.example.test", "port": 443, "result": "BYPASS", "reason": "temporary-rule"},
        ],
    )
    write_jsonl(
        "incident/vpn.jsonl",
        [
            {"start": "2026-08-15T14:00:00Z", "end": "2026-08-15T18:00:00Z", "user": "contractor", "assigned_ip": "10.0.250.12", "source_ip": "203.0.113.88", "result": "success"},
        ],
    )
    write_jsonl(
        "incident/siem.jsonl",
        [
            {"time": "2026-08-15T16:04:10Z", "rule": "WORKSTATION-SMB-FANOUT", "severity": "high", "entity": "ws-23", "source_events": ["flow", "endpoint"], "status": "new"},
        ],
    )
    write_text(
        "incident/evidence-ledger-template.csv",
        "evidence_id,source,collection_point,raw_time,normalized_time,entity,observation,classification,limitation,confidence\n",
    )


def build_challenge_fixtures() -> None:
    """Package existing evidence and two explicitly authored transfer cases."""
    transfer = FIXTURES / "challenges" / "transfer.pcap"
    transfer.parent.mkdir(parents=True, exist_ok=True)
    transfer.write_bytes((FIXTURES / "pcaps" / "mtu-failure.pcap").read_bytes())
    rounds = (
        ("incident/assets.json", "incident/siem.jsonl", "incident/flows.jsonl"),
        ("incident/dns.jsonl", "incident/endpoint.jsonl", "incident/auth.jsonl"),
        ("incident/firewall.jsonl", "incident/proxy.jsonl", "routing/vrfs.json"),
    )
    for number, sources in enumerate(rounds, 1):
        evidence = {}
        for source in sources:
            raw = (FIXTURES / source).read_text()
            evidence[source] = (
                [json.loads(line) for line in raw.splitlines()]
                if source.endswith(".jsonl") else json.loads(raw)
            )
        write_json(f"challenges/incident-round-{number}.json", evidence)

    write_json(
        "challenges/case-a.json",
        {
            "case": "A-v1",
            "brief": "An approved cloud-to-server health check stops after a routing change.",
            "scope": "Independent drill on the reference network, not part of the incident timeline.",
            "flow": {"src": "10.20.5.10", "dst": "10.0.20.40", "protocol": "tcp", "sport": 56000, "dport": 443},
            "path": ["corp-vpc", "hybrid-link", "on-prem-firewall", "file-01"],
            "conditions": {
                "route_tables_complete_for_this_flow": True,
                "firewall": "Allows this flow and established return traffic; state is healthy.",
                "nat": False,
                "link": "Up in both directions; no recorded link change during the drill.",
                "server": "TCP/443 listener healthy; TLS and application success must still be tested.",
                "change_owner": "network-operations",
                "clock": "All records synchronized to UTC within 1 ms; event spacing exceeds that tolerance.",
            },
            "before": {
                "time": "2026-08-16T09:59:00Z",
                "routes": {
                    "corp-vpc": [{"prefix": "10.0.0.0/8", "next_hop": "on-prem"}],
                    "on-prem": [
                        {"prefix": "10.0.20.0/24", "next_hop": "connected"},
                        {"prefix": "10.20.0.0/16", "next_hop": "corp-vpc"},
                    ],
                },
                "health_check": "HTTP 200 over TLS",
            },
            "after": {
                "time": "2026-08-16T10:00:00Z",
                "routes": {
                    "corp-vpc": [{"prefix": "10.0.0.0/8", "next_hop": "on-prem"}],
                    "on-prem": [{"prefix": "10.0.20.0/24", "next_hop": "connected"}],
                },
            },
            "observations": [
                {"id": "A1", "time": "2026-08-16T10:00:01.000Z", "sensor": "corp-vpc-egress", "event": "SYN sent", "src": "10.20.5.10", "dst": "10.0.20.40"},
                {"id": "A2", "time": "2026-08-16T10:00:01.020Z", "sensor": "file-01-host", "event": "SYN received; SYN-ACK emitted", "src": "10.20.5.10", "dst": "10.0.20.40"},
                {"id": "A3", "time": "2026-08-16T10:00:01.030Z", "sensor": "on-prem-router", "event": "drop: no matching route", "src": "10.0.20.40", "dst": "10.20.5.10"},
                {"id": "A4", "time": "2026-08-16T10:00:04.000Z", "sensor": "client-host", "event": "connection timeout; no SYN-ACK received"},
            ],
            "limitations": ["No audit record establishes why the route changed.", "No post-repair packet or application observation is supplied."],
        },
    )
    write_json(
        "challenges/case-b.json",
        {
            "case": "B-v1",
            "brief": "An approved workstation diagnostic connection stops after an interface reassignment.",
            "scope": "Independent drill. The explicit test permission replaces the incident's egress intent for this flow only.",
            "flow": {"src": "10.0.10.23", "dst": "198.51.100.77", "protocol": "tcp", "sport": 57000, "dport": 443},
            "path": ["ws-23", "context-router", "enterprise-firewall", "external-test-service"],
            "conditions": {
                "route_tables_complete_for_this_flow": True,
                "route_leaking": False,
                "policy": "Approved diagnostic TCP/443 flow; firewall permits it if reached, with healthy NAT/session state.",
                "nat": "At enterprise-firewall only: 10.0.10.23 to 192.0.2.44.",
                "return": "External service returns to 192.0.2.44; firewall has routes to the client prefix in both contexts.",
                "link": "Client link and gateway neighbor remain healthy.",
                "change_owner": "network-operations",
                "clock": "All records synchronized to UTC within 1 ms; event spacing exceeds that tolerance.",
            },
            "routes": {
                "CORP": [
                    {"prefix": "10.0.10.0/24", "next_hop": "connected"},
                    {"prefix": "0.0.0.0/0", "next_hop": "enterprise-firewall"},
                ],
                "ISOLATED": [{"prefix": "10.0.10.0/24", "next_hop": "connected"}],
            },
            "before": {"time": "2026-08-16T10:59:00Z", "ingress_vrf": "CORP", "health_check": "HTTP 200 over TLS"},
            "after": {"time": "2026-08-16T11:00:00Z", "ingress_vrf": "ISOLATED"},
            "observations": [
                {"id": "B1", "time": "2026-08-16T11:00:01.000Z", "sensor": "client-host", "event": "SYN emitted", "src": "10.0.10.23", "dst": "198.51.100.77"},
                {"id": "B2", "time": "2026-08-16T11:00:01.010Z", "sensor": "context-router", "event": "ingress SYN; lookup has no matching prefix", "vrf": "ISOLATED", "dst": "198.51.100.77"},
                {"id": "B3", "time": "2026-08-16T11:00:04.000Z", "sensor": "enterprise-firewall", "event": "no matching session in this three-second window", "coverage": "Full session table checked; no session creation observed."},
            ],
            "limitations": ["No change ticket says whether reassignment was intentional containment.", "No evidence supports compromise or a firewall deny for this attempt."],
        },
    )
    write_json(
        "challenges/evidence-map.json",
        {
            "transfer.pcap": {"source": "pcaps/mtu-failure.pcap", "sha256": hashlib.sha256(transfer.read_bytes()).hexdigest(), "collection_point": "Modeled VLAN 10 trunk", "limitation": "ICMP visible here does not prove receipt or handling by the sender."},
            "incident_rounds": {str(n): list(sources) for n, sources in enumerate(rounds, 1)},
            "case-a.json": {"source": "Authored independent drill A-v1", "collection_points": ["cloud egress", "server host", "on-prem router", "client host"]},
            "case-b.json": {"source": "Authored independent drill B-v1", "collection_points": ["client host", "context router", "firewall session table"]},
            "integrity": "All challenge files and original source files are covered by the parent fixture manifest.",
            "independence": "Round files are copies of original records, not additional sensors. Zeek is derived from incident.pcap; SIEM lists flow and endpoint dependencies.",
        },
    )


def build_manifest() -> None:
    files = []
    for path in sorted(FIXTURES.rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            files.append(
                {
                    "path": str(path.relative_to(FIXTURES)),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                }
            )
    write_json(
        "manifest.json",
        {
            "case": "network-bootcamp-reference",
            "generated_at": "2026-08-15T00:00:00Z",
            "files": files,
        },
    )


def build_extension_fixtures() -> None:
    """Independent authored comparisons, never additional original incident facts."""
    write_json("network/troubleshooting.json", {
        "scope": "Independent saved teaching comparisons; not live measurements or factory incident events.",
        "dns": [
            {"id": "D1", "query": "missing.example.test", "type": "A", "resolver": "192.0.2.53", "client_observation": "query sent; no response in 3 seconds", "rcode": None, "answers": None},
            {"id": "D2", "query": "missing.example.test", "type": "A", "resolver": "192.0.2.53", "client_observation": "response received", "rcode": "NXDOMAIN", "answers": []},
            {"id": "D3", "query": "v4-only.example.test", "type": "AAAA", "resolver": "192.0.2.53", "client_observation": "response received", "rcode": "NOERROR", "answers": [], "authority": "SOA example.test; no referral"},
            {"id": "D4", "query": "app.example.test", "type": "A", "resolver": "192.0.2.53", "client_observation": "response received; TCP handshake complete; HTTP 503", "rcode": "NOERROR", "answers": ["192.0.2.40"]},
        ],
        "attachment_conditions": {"interface": "en0", "address": "192.0.2.23/24", "gateway": "192.0.2.1", "expected_access_vlan": 10, "counter_interval_seconds": 10, "counter_semantics": "deltas during this isolated authorized test", "server": "192.0.2.40:443"},
        "attachment": [
            {"id": "L1", "link": "down", "access_vlan": 10, "rx_frames": 0, "rx_errors": 0, "gateway_neighbor": "INCOMPLETE", "switch_mac": None, "test": "no reply"},
            {"id": "L2", "link": "up", "access_vlan": 20, "rx_frames": 15, "rx_errors": 0, "gateway_neighbor": "INCOMPLETE", "switch_mac": "client learned in VLAN 20", "test": "no ARP reply"},
            {"id": "L3", "link": "up", "access_vlan": 10, "rx_frames": 15, "rx_errors": 0, "gateway_neighbor": "INCOMPLETE", "switch_mac": "client learned in VLAN 10", "test": "ARP request seen; peer reply absent; peer state not supplied"},
            {"id": "L4", "link": "up", "access_vlan": 10, "rx_frames": 25, "rx_errors": 0, "gateway_neighbor": "REACHABLE", "server_neighbor": "REACHABLE", "switch_mac": "client learned in VLAN 10", "test": "server receives SYN and emits RST; authorized host socket inventory shows no TCP/443 listener"},
        ],
    })
    write_json("architecture/performance.json", {
        "scope": "Independent synthetic saved measurements for comparison; not wan.json observations.",
        "method": "One TCP stream, same endpoints and payload, 60-second receive interval after warmup; no TLS; all rates decimal Mbps.",
        "interval_seconds": 60,
        "probe_count": 60,
        "probe_method": "One probe per second. Loss percentages rounded to two decimal places; rtt_ms is the median of received replies.",
        "jitter_definition": "Mean absolute RTT difference for adjacent sent probes only when both received a reply; exclude pairs containing a lost probe. RTT variation, not one-way RTP jitter.",
        "measurements": [
            {"id": "P1", "capacity_mbps": 200, "received_bytes": 1125000000, "goodput_mbps": 150, "rtt_ms": 20, "probe_lost": 0, "probe_loss_percent": 0, "rtt_jitter_ms": 1, "receiver_window_bytes": 2000000},
            {"id": "P2", "capacity_mbps": 200, "received_bytes": 262500000, "goodput_mbps": 35, "rtt_ms": 20, "probe_lost": 1, "probe_loss_percent": 1.67, "rtt_jitter_ms": 12, "receiver_window_bytes": 2000000},
            {"id": "P3", "capacity_mbps": 200, "received_bytes": 300000000, "goodput_mbps": 40, "rtt_ms": 80, "probe_lost": 0, "probe_loss_percent": 0, "rtt_jitter_ms": 1, "receiver_window_bytes": 400000},
        ],
        "backup": {"capacity_mbps": 200, "demands_mbps": {"process_reporting": 120, "voice_and_operations": 40, "bulk_replication": 60}, "overhead_and_other_load_mbps": None},
        "limits": "Probe loss need not equal TCP loss. Congestion window, receiver CPU, disk, and competing load are unmeasured. A correlation suggests a check, not a unique cause.",
    })
    write_json("challenges/recovery.json", {
        "scope": "Separate hypothetical epilogues; open only after both assessed A/B attempts. These are new conditions, not historical evidence for the original cases or incident.",
        "A": {
            "change": {"id": "RA1", "time": "2026-08-16T10:10:00Z", "owner": "network-operations", "approval": "service owner approves restoring the removed return route", "action": "restore on-prem 10.20.0.0/16 via corp-vpc", "rollback": "restore the prior table if unrelated traffic changes"},
            "before": {"id": "RA2", "result": "client timeout; see original A1-A4 only for pre-repair evidence"},
            "after": {"id": "RA3", "sensor": "client application and server request logs", "window": "10:10:10Z through 10:15:00Z", "result": "30 of 30 health checks complete TLS and HTTP 200; request IDs agree at client and server"},
            "acceptance": {"id": "RA4", "owner": "production-reporting service owner", "result": "accepts restoration of the scoped health-check service", "remaining_risk": "change cause and other services remain unverified"},
        },
        "B": {
            "change": {"id": "RB1", "time": "2026-08-16T11:10:00Z", "owner": "network-operations", "approval": "owner confirms reassignment was accidental and approves restoring CORP for the diagnostic", "action": "restore client ingress to CORP", "rollback": "restore prior assignment if the approved diagnostic scope is exceeded"},
            "before": {"id": "RB2", "result": "no matching destination prefix; original B1-B3 describe pre-repair state"},
            "after": {"id": "RB3", "sensor": "client and external test-service application logs", "window": "11:10:10Z through 11:15:00Z", "result": "30 of 30 TCP and TLS exchanges complete; 30 HTTP 503 responses; service log says backend unavailable"},
            "acceptance": {"id": "RB4", "owner": "diagnostic service owner", "result": "route restoration accepted; service restoration rejected; application team owns backend investigation", "remaining_risk": "backend cause unknown; retain scoped permission and monitoring"},
        },
    })


def build() -> None:
    build_foundations()
    build_mtu_failure()
    build_incident()
    build_text_fixtures()
    build_challenge_fixtures()
    build_extension_fixtures()
    build_manifest()


def check() -> list[str]:
    errors = []
    manifest_path = FIXTURES / "manifest.json"
    if not manifest_path.exists():
        return ["missing labs/fixtures/manifest.json; run the builder"]
    manifest = json.loads(manifest_path.read_text())
    listed = {entry["path"] for entry in manifest["files"]}
    actual = {
        str(path.relative_to(FIXTURES))
        for path in FIXTURES.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    for path in sorted(actual - listed):
        errors.append(f"untracked fixture {path}")
    for path in sorted(listed - actual):
        errors.append(f"missing {path}")
    for entry in manifest["files"]:
        path = FIXTURES / entry["path"]
        if not path.exists():
            errors.append(f"missing {entry['path']}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry["sha256"]:
            errors.append(f"checksum mismatch {entry['path']}")
    for path in FIXTURES.rglob("*.json"):
        try:
            json.loads(path.read_text())
        except json.JSONDecodeError as error:
            errors.append(f"invalid JSON {path.relative_to(FIXTURES)}: {error}")
    for path in FIXTURES.rglob("*.jsonl"):
        for number, line in enumerate(path.read_text().splitlines(), 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"invalid JSON {path.name}:{number}: {error}")
    for name in ("foundations.pcap", "mtu-failure.pcap", "incident.pcap"):
        path = FIXTURES / "pcaps" / name
        if not path.exists() or path.read_bytes()[:4] != b"\xd4\xc3\xb2\xa1":
            errors.append(f"invalid PCAP {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        build()
    errors = check()
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    count = len(json.loads((FIXTURES / "manifest.json").read_text())["files"])
    print(f"fixtures ready: {count} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
