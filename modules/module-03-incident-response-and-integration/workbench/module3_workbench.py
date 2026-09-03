#!/usr/bin/env python3
"""Interactive, fixture-backed practice for Module 3."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from datetime import datetime
from pathlib import Path


ACTIVITIES = {
    "telemetry": "source strengths, limitations, and independence",
    "timeline": "multi-source event ordering and intervals",
    "correlation": "entities, processes, sessions, and detections",
    "claims": "observation, inference, hypothesis, and unknown",
    "scope": "confirmed systems, identities, boundaries, and gaps",
}

LOGS = {
    "dns": "incident/dns.jsonl",
    "flow": "incident/flows.jsonl",
    "firewall": "incident/firewall.jsonl",
    "auth": "incident/auth.jsonl",
    "endpoint": "incident/endpoint.jsonl",
    "proxy": "incident/proxy.jsonl",
    "vpn": "incident/vpn.jsonl",
    "siem": "incident/siem.jsonl",
}

LEDGER_FIELDS = [
    "evidence_id",
    "source",
    "collection_point",
    "raw_time",
    "normalized_time",
    "entity",
    "observation",
    "classification",
    "limitation",
    "confidence",
]


def repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "labs" / "fixtures" / "manifest.json").is_file():
            return parent
    raise SystemExit("error: run this script from inside the network_bootcamp repository")


ROOT = repository_root()
FIXTURES = ROOT / "labs" / "fixtures"


def read_json(relative: str):
    with (FIXTURES / relative).open(encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(relative: str) -> list[dict]:
    with (FIXTURES / relative).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def normalize(value: str) -> str:
    value = value.strip().lower().replace("->", " ").replace(",", " ")
    return " ".join(value.split())


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def question(
    activity: str,
    prompt: str,
    answer: str,
    explanation: str,
    evidence: str,
    aliases: tuple[str, ...] = (),
) -> dict:
    answers = {normalize(answer), *(normalize(alias) for alias in aliases)}
    return {
        "activity": activity,
        "prompt": prompt,
        "answer": answer,
        "answers": answers,
        "explanation": explanation,
        "evidence": evidence,
    }


def load_logs() -> dict[str, list[dict]]:
    return {source: read_jsonl(relative) for source, relative in LOGS.items()}


def event_time(source: str, record: dict) -> str:
    return record["start"] if source in {"flow", "vpn"} else record["time"]


def event_entity(source: str, record: dict) -> str:
    fields = {
        "dns": "client",
        "flow": "src",
        "firewall": "src",
        "auth": "host",
        "endpoint": "host",
        "proxy": "client",
        "vpn": "user",
        "siem": "entity",
    }
    return str(record[fields[source]])


def event_observation(source: str, record: dict) -> str:
    if source == "dns":
        return f"DNS {record['client']} queried {record['query']} -> {record['answer']}"
    if source == "flow":
        return (
            f"flow {record['src']}:{record['sport']} -> "
            f"{record['dst']}:{record['dport']} bytes={record['bytes']} end={record['end']}"
        )
    if source == "firewall":
        return (
            f"firewall {record['action']} {record['rule']} "
            f"{record['src']} -> {record['dst']}:{record['dport']}"
        )
    if source == "auth":
        origin = f" from {record['source']}" if "source" in record else ""
        return f"auth {record['result']} {record['user']} -> {record['host']}{origin}"
    if source == "endpoint":
        detail = record.get("process") or record["event"]
        if "query" in record:
            detail += f" -> {record['query']}"
        return f"endpoint {record['event']} {record['host']} {detail}"
    if source == "proxy":
        return f"proxy {record['result']} {record['client']} -> {record['host']}:{record['port']}"
    if source == "vpn":
        return (
            f"VPN {record['result']} {record['user']} -> {record['assigned_ip']} "
            f"end={record['end']}"
        )
    return f"SIEM {record['severity']} {record['rule']} for {record['entity']}"


def build_timeline(logs: dict[str, list[dict]] | None = None) -> list[dict]:
    logs = logs or load_logs()
    events = []
    for source, records in logs.items():
        for number, record in enumerate(records, 1):
            raw_time = event_time(source, record)
            events.append(
                {
                    "time": raw_time,
                    "source": source,
                    "record": number,
                    "entity": event_entity(source, record),
                    "observation": event_observation(source, record),
                }
            )
    return sorted(events, key=lambda event: (parse_time(event["time"]), event["source"]))


def print_timeline(source: str | None) -> int:
    events = build_timeline()
    if source:
        events = [event for event in events if event["source"] == source]
    print("Normalized incident timeline")
    print(f"Events: {len(events)}" + (f" | Source: {source}" if source else ""))
    print("Equal timestamps are peers; display order does not prove causal order.")
    for event in events:
        print(
            f"{event['time']}  {event['source']:8}  "
            f"record {event['record']:>2}  {event['observation']}"
        )
    return 0


def telemetry_questions(logs: dict[str, list[dict]]) -> list[dict]:
    return [
        question(
            "telemetry",
            "Which source directly associates update-agent with the DNS query?",
            "endpoint",
            "The endpoint record contains both process and query; DNS logs contain the client but not its process.",
            "incident/endpoint.jsonl: record 2",
        ),
        question(
            "telemetry",
            "Which source records the translated source address for the external TLS session?",
            "firewall",
            "The firewall session includes translated_src 192.0.2.44.",
            "incident/firewall.jsonl: record 1",
        ),
        question(
            "telemetry",
            "Is the SIEM alert independent corroboration of its flow and endpoint source events? (yes/no)",
            "no",
            "The SIEM record declares flow and endpoint as source_events, so it is derived from them.",
            "incident/siem.jsonl: record 1",
            ("n",),
        ),
        question(
            "telemetry",
            "Which source records the hostname and a BYPASS result for the outbound connection?",
            "proxy",
            "The proxy record supplies the requested host, result, and temporary-rule reason.",
            "incident/proxy.jsonl: record 1",
        ),
        question(
            "telemetry",
            "Which source reports connection byte counts but does not identify a process?",
            "flow",
            "Flow records contain tuples, times, and byte totals; process attribution requires endpoint evidence.",
            "incident/flows.jsonl: records 1-4",
            ("flows", "netflow"),
        ),
    ]


def timeline_questions(logs: dict[str, list[dict]]) -> list[dict]:
    external = sorted(
        (record for record in logs["flow"] if record["dst"] == "198.51.100.77"),
        key=lambda record: parse_time(record["start"]),
    )
    interval = int((parse_time(external[1]["start"]) - parse_time(external[0]["start"])).total_seconds())
    process = next(record for record in logs["endpoint"] if record.get("process") == "update-agent")
    child = next(record for record in logs["endpoint"] if record.get("process") == "smb-client")
    alert = logs["siem"][0]
    return [
        question(
            "timeline",
            "Which process starts immediately before the first cdn-update DNS evidence?",
            process["process"],
            f"The process starts at {process['time']}, two seconds before the DNS records.",
            "incident/endpoint.jsonl: record 1",
        ),
        question(
            "timeline",
            "How many seconds separate the starts of the first two external TLS flows?",
            str(interval),
            "The external flow starts are 16:01:00, 16:02:00, and 16:03:00 UTC.",
            "incident/flows.jsonl: records 1-3",
            (f"{interval} seconds", "1 minute"),
        ),
        question(
            "timeline",
            "Which child process appears one second before the SMB flow starts?",
            child["process"],
            "smb-client starts at 16:03:59 and the SMB flow starts at 16:04:00.",
            "incident/endpoint.jsonl: record 3 and incident/flows.jsonl: record 4",
        ),
        question(
            "timeline",
            "After the SMB flow starts, which source records first: auth or firewall?",
            "auth",
            "Authentication is recorded at 16:04:01; the firewall allow follows at 16:04:02.",
            "incident/auth.jsonl: record 2 and incident/firewall.jsonl: record 2",
        ),
        question(
            "timeline",
            "At what UTC time is the SIEM alert created?",
            alert["time"],
            "The alert follows the SMB process, flow, authentication, and firewall evidence.",
            "incident/siem.jsonl: record 1",
            ("16:04:10Z", "16:04:10"),
        ),
    ]


def correlation_questions(logs: dict[str, list[dict]]) -> list[dict]:
    dns = logs["dns"][0]
    endpoint_dns = next(record for record in logs["endpoint"] if record["event"] == "dns_query")
    firewall = logs["firewall"][0]
    auth = next(record for record in logs["auth"] if record["method"] == "network")
    siem = logs["siem"][0]
    return [
        question(
            "correlation",
            f"Which address does {dns['query']} resolve to?",
            dns["answer"],
            "The DNS answer supplies the address later used by all three external flows.",
            "incident/dns.jsonl: record 1",
        ),
        question(
            "correlation",
            "Which process issued the endpoint-recorded cdn-update query?",
            endpoint_dns["process"],
            "The endpoint event connects update-agent to the query on ws-23.",
            "incident/endpoint.jsonl: record 2",
        ),
        question(
            "correlation",
            "What translated source address is assigned to the external firewall session?",
            firewall["translated_src"],
            "This mapping explains why a downstream source may differ from ws-23's local address.",
            "incident/firewall.jsonl: record 1",
        ),
        question(
            "correlation",
            "What result does the proxy record for cdn-update.example.test?",
            logs["proxy"][0]["result"],
            "BYPASS explains why normal proxy inspection may not cover the connection.",
            "incident/proxy.jsonl: record 1",
        ),
        question(
            "correlation",
            "Which account successfully authenticates to file-01 from 10.0.10.23?",
            auth["user"],
            "The authentication record supplies user, target host, source, method, and result.",
            "incident/auth.jsonl: record 2",
        ),
        question(
            "correlation",
            "Which SIEM rule creates the alert for ws-23?",
            siem["rule"],
            "The rule name is an alerting label; it is not proof of lateral movement.",
            "incident/siem.jsonl: record 1",
        ),
        question(
            "correlation",
            "Which two source types feed the SIEM alert?",
            "flow and endpoint",
            "Those sources support the alert but also show why the alert is not independent evidence.",
            "incident/siem.jsonl: record 1 source_events",
            ("flow endpoint", "endpoint and flow"),
        ),
    ]


def claim_questions() -> list[dict]:
    suffix = " Classify it as observed, inferred, hypothesized, or unknown."
    return [
        question(
            "claims",
            "The DNS log records cdn-update.example.test returning 198.51.100.77." + suffix,
            "observed",
            "The exact query and answer appear directly in a DNS record.",
            "incident/dns.jsonl: record 1",
        ),
        question(
            "claims",
            "update-agent generated the three external TLS connections." + suffix,
            "inferred",
            "Process and DNS timing support this link, but no fixture maps the sockets directly to the process.",
            "incident/endpoint.jsonl and incident/flows.jsonl",
        ),
        question(
            "claims",
            "The periodic external TLS traffic is malicious command and control." + suffix,
            "hypothesized",
            "Periodicity is consistent with beaconing and legitimate update checks; intent is not observed.",
            "incident/flows.jsonl: records 1-3",
        ),
        question(
            "claims",
            "Credentials were stolen from alex or svc-backup." + suffix,
            "unknown",
            "The fixtures show authentication behavior but no credential-theft evidence.",
            "incident/auth.jsonl and incident/endpoint.jsonl",
        ),
        question(
            "claims",
            "svc-backup successfully authenticated to file-01 from 10.0.10.23." + suffix,
            "observed",
            "All parts of the statement are fields in the network-authentication record.",
            "incident/auth.jsonl: record 2",
        ),
    ]


def scope_questions(logs: dict[str, list[dict]]) -> list[dict]:
    assets = read_json("incident/assets.json")
    denied = next(record for record in logs["firewall"] if record["action"] == "deny")
    workstation = assets["10.0.10.23"]
    server = assets["10.0.20.40"]
    return [
        question(
            "scope",
            "Which host is directly tied to process, DNS, external flow, SMB, and SIEM evidence?",
            workstation["host"],
            "The sources repeatedly identify ws-23 or its address 10.0.10.23.",
            "incident/assets.json and incident/*.jsonl",
        ),
        question(
            "scope",
            "Who owns the primary workstation in the asset record?",
            workstation["owner"],
            "Ownership is context for coordination, not proof of who caused the activity.",
            "incident/assets.json: 10.0.10.23.owner",
        ),
        question(
            "scope",
            "Which host receives the successful SMB authentication?",
            server["host"],
            "The asset and authentication records identify 10.0.20.40 as file-01.",
            "incident/assets.json and incident/auth.jsonl: record 2",
        ),
        question(
            "scope",
            "Which OT destination is denied for direct access from ws-23?",
            denied["dst"],
            "The deny record names the destination and creates no session.",
            "incident/firewall.jsonl: record 3",
        ),
        question(
            "scope",
            "Does any fixture prove successful direct access from ws-23 to the OT destination? (yes/no)",
            "no",
            "The only direct user-to-OT record is a deny; successful OT access remains unproven.",
            "incident/firewall.jsonl: record 3",
            ("n",),
        ),
        question(
            "scope",
            "Does the evidence prove persistence or data exfiltration? (yes/no)",
            "no",
            "No persistence mechanism, transferred file, or outbound data volume proving exfiltration appears.",
            "incident/endpoint.jsonl and incident/flows.jsonl",
            ("n",),
        ),
    ]


def all_questions() -> dict[str, list[dict]]:
    logs = load_logs()
    return {
        "telemetry": telemetry_questions(logs),
        "timeline": timeline_questions(logs),
        "correlation": correlation_questions(logs),
        "claims": claim_questions(),
        "scope": scope_questions(logs),
    }


def choose_questions(activity: str, seed: int, limit: int | None) -> list[dict]:
    groups = all_questions()
    selected = sum(groups.values(), []) if activity == "all" else list(groups[activity])
    random.Random(seed).shuffle(selected)
    return selected[:limit] if limit else selected


def show_question(item: dict, number: int, reveal: bool) -> bool:
    print(f"\n{number}. [{item['activity']}] {item['prompt']}")
    print(f"   Evidence: labs/fixtures/{item['evidence']}")
    if reveal:
        correct = True
    else:
        try:
            response = input("   Your answer: ")
        except EOFError:
            raise SystemExit("\nerror: input ended before the activity was complete") from None
        correct = normalize(response) in item["answers"]
        print("   Correct." if correct else f"   Not yet. Expected: {item['answer']}")
    print(f"   Answer: {item['answer']}")
    print(f"   Why: {item['explanation']}")
    return correct


def run_session(activity: str, seed: int, limit: int | None, reveal: bool) -> int:
    selected = choose_questions(activity, seed, limit)
    label = "Demonstration" if reveal else "Practice"
    print(f"Module 3 Workbench — {label}")
    print(f"Seed: {seed} | Questions: {len(selected)}")
    score = sum(show_question(item, number, reveal) for number, item in enumerate(selected, 1))
    if not reveal:
        print(f"\nScore: {score}/{len(selected)}")
        print("Review each cited fixture before retrying with the same seed.")
    return 0


def verify_manifest() -> None:
    manifest = read_json("manifest.json")
    entries = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    used = ("incident/assets.json", *LOGS.values(), "incident/evidence-ledger-template.csv")
    for relative in used:
        actual = hashlib.sha256((FIXTURES / relative).read_bytes()).hexdigest()
        assert entries[relative] == actual, f"fixture checksum mismatch: {relative}"


def self_test() -> int:
    verify_manifest()
    with (FIXTURES / "incident" / "evidence-ledger-template.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        assert next(csv.reader(handle)) == LEDGER_FIELDS

    logs = load_logs()
    timeline = build_timeline(logs)
    assert len(timeline) == 17
    assert timeline[0]["source"] == "vpn"
    assert timeline[-1]["time"] == "2026-08-15T16:10:00.000Z"

    external = [record for record in logs["flow"] if record["dst"] == "198.51.100.77"]
    starts = [parse_time(record["start"]) for record in external]
    assert [(right - left).total_seconds() for left, right in zip(starts, starts[1:])] == [60, 60]
    assert logs["firewall"][2]["action"] == "deny"
    assert logs["auth"][1]["user"] == "svc-backup"
    assert logs["siem"][0]["source_events"] == ["flow", "endpoint"]

    groups = all_questions()
    assert set(groups) == set(ACTIVITIES)
    assert all(len(items) >= 5 for items in groups.values())
    assert all(normalize(item["answer"]) in item["answers"] for items in groups.values() for item in items)
    fixture_count = len(("incident/assets.json", *LOGS.values(), "incident/evidence-ledger-template.csv"))
    print(
        f"self-test passed: {sum(map(len, groups.values()))} questions, "
        f"{fixture_count} fixtures verified, {len(timeline)} timeline events"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest="command", required=True)
    subcommands.add_parser("list", help="list available activities")
    timeline = subcommands.add_parser("timeline", help="print the normalized evidence timeline")
    timeline.add_argument("--source", choices=tuple(LOGS), help="show one source only")
    subcommands.add_parser("self-test", help="verify fixtures and workbench logic")
    for name, help_text in (("demo", "reveal worked answers"), ("run", "start scored practice")):
        command = subcommands.add_parser(name, help=help_text)
        command.add_argument("activity", nargs="?", choices=("all", *ACTIVITIES), default="all")
        command.add_argument("--seed", type=int, default=1, help="reproducible question order")
        command.add_argument("--limit", type=int, help="maximum number of questions")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "list":
        print("Module 3 Workbench activities:")
        for name, description in ACTIVITIES.items():
            print(f"  {name:12} {description}")
        return 0
    if args.command == "timeline":
        return print_timeline(args.source)
    if args.command == "self-test":
        return self_test()
    if args.limit is not None and args.limit < 1:
        raise SystemExit("error: --limit must be at least 1")
    return run_session(args.activity, args.seed, args.limit, args.command == "demo")


if __name__ == "__main__":
    sys.exit(main())
