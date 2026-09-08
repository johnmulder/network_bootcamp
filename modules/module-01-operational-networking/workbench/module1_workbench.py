#!/usr/bin/env python3
"""Interactive, fixture-backed practice for Module 1."""

from __future__ import annotations

import argparse
import csv
import hashlib
import ipaddress
import json
import random
import sys
from datetime import datetime
from pathlib import Path


ACTIVITIES = {
    "l2": "VLAN, STP, and LACP evidence",
    "routes": "longest-prefix route selection",
    "convergence": "failure timing and changed route decisions",
    "services": "DHCP state and dependencies",
    "vrf": "routing-context reachability",
    "troubleshooting": "evidence-driven diagnosis",
}


def repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "course.py").is_file():
            return parent
    raise SystemExit("error: run this script from inside the network_bootcamp repository")


ROOT = repository_root()
sys.path.insert(0, str(ROOT))
import learning
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


def question(
    activity: str,
    prompt: str,
    answer: str,
    explanation: str,
    evidence: str,
    aliases: tuple[str, ...] = (),
    *,
    question_id: str,
) -> dict:
    answers = {normalize(answer), *(normalize(alias) for alias in aliases)}
    return {
        "id": question_id,
        "activity": activity,
        "prompt": prompt,
        "answer": answer,
        "answers": answers,
        "explanation": explanation,
        "evidence": evidence,
    }


def l2_questions() -> list[dict]:
    data = read_json("network/l2-control.json")
    stp = data["stp"]
    discarded = next(link for link in stp["links"] if "discarding" in link["state"])
    discarded_suffix = discarded["state"].removeprefix("discarding-on-")
    discarded_bridge = next(
        endpoint for endpoint in (discarded["a"], discarded["b"]) if endpoint.endswith(discarded_suffix)
    )
    flow = next(item for item in data["lacp"]["flows"] if "10.0.10.24" in item["tuple"])
    return [
        question(
            "l2",
            "Which bridge is the STP root?",
            stp["root"],
            "The root field names the elected bridge; bridge priority confirms why it wins.",
            "network/l2-control.json: .stp.root and .stp.bridges",
            question_id='m1.l2.root',
        ),
        question(
            "l2",
            "Which endpoint discards on the redundant access-to-access link?",
            discarded_bridge,
            "One side discards so the redundant triangle does not form a forwarding loop.",
            "network/l2-control.json: .stp.links[]",
            question_id='m1.l2.discarding',
        ),
        question(
            "l2",
            "Which VLAN ID represents the SERVERS subnet?",
            next(vlan for vlan, details in data["vlans"].items() if details["name"] == "SERVERS"),
            "The VLAN map associates SERVERS with subnet 10.0.20.0/24.",
            "network/l2-control.json: .vlans",
            question_id='m1.l2.servers-vlan',
        ),
        question(
            "l2",
            f"Which LACP member carries {flow['tuple']}?",
            flow["member"],
            "A link aggregate normally keeps one flow on one selected member.",
            "network/l2-control.json: .lacp.flows[]",
            question_id='m1.l2.lacp-member',
        ),
    ]


def route_rows() -> list[dict]:
    with (FIXTURES / "routing" / "route-candidates.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        return list(csv.DictReader(line for line in handle if line.strip()))


def select_routes(destination: str, rows: list[dict]) -> list[dict]:
    address = ipaddress.ip_address(destination)
    matches = [row for row in rows if address in ipaddress.ip_network(row["prefix"])]
    if not matches:
        return []
    longest = max(ipaddress.ip_network(row["prefix"]).prefixlen for row in matches)
    matches = [
        row for row in matches if ipaddress.ip_network(row["prefix"]).prefixlen == longest
    ]
    preference = min(int(row["preference"]) for row in matches)
    matches = [row for row in matches if int(row["preference"]) == preference]
    metric = min(int(row["metric"]) for row in matches)
    return [row for row in matches if int(row["metric"]) == metric]


def route_questions() -> list[dict]:
    rows = route_rows()
    result = []
    for destination in (
        "10.0.20.40",
        "10.0.20.99",
        "198.51.100.77",
        "203.0.113.10",
    ):
        selected = select_routes(destination, rows)
        prefix = selected[0]["prefix"]
        next_hops = ", ".join(row["next_hop"] for row in selected)
        result.append(
            question(
                "routes",
                f"Which prefix wins the route lookup for {destination}?",
                prefix,
                f"Longest-prefix match selects {prefix}; the selected next hop(s) are {next_hops}.",
                "routing/route-candidates.csv",
                question_id=f"m1.routes.{destination}",
            )
        )
    return result


def convergence_questions() -> list[dict]:
    events = read_jsonl("routing/route-events.jsonl")
    detected = next(event for event in events if event["event"] == "link_down")
    installed = next(event for event in events if event["event"] == "fib_install")
    elapsed = (
        datetime.fromisoformat(installed["time"].replace("Z", "+00:00"))
        - datetime.fromisoformat(detected["time"].replace("Z", "+00:00"))
    )
    milliseconds = round(elapsed.total_seconds() * 1000)
    remaining = [row for row in route_rows() if row["prefix"] != "10.0.20.40/32"]
    prefix = select_routes("10.0.20.40", remaining)[0]["prefix"]
    return [
        question(
            "convergence",
            "How many milliseconds pass from logged link-down to FIB installation?",
            str(milliseconds),
            "This measures the logged forwarding-table update, not detection delay or application recovery.",
            "routing/route-events.jsonl: link_down and fib_install",
            (f"{milliseconds} ms",),
            question_id='m1.convergence.interval',
        ),
        question(
            "convergence",
            "Which next hop is installed after the modeled link failure?",
            installed["next_hop"],
            "The installation event names the remaining forwarding choice.",
            "routing/route-events.jsonl: fib_install.next_hop",
            question_id='m1.convergence.next-hop',
        ),
        question(
            "convergence",
            "Does a FIB installation timestamp alone prove application recovery? (yes/no)",
            "no",
            "Observe packets, session state, and an application response to establish service recovery.",
            "routing/route-events.jsonl: recorded event types",
            ("n",),
            question_id='m1.convergence.application',
        ),
        question(
            "convergence",
            "In the independent CSV snapshot, remove only 10.0.20.40/32. Which prefix now wins for 10.0.20.40?",
            prefix,
            "The two remaining /24 routes beat /8 and default by destination specificity; a flow's actual ECMP member is not shown.",
            "routing/route-candidates.csv: hypothetical removal of the .40/32 row",
            question_id='m1.convergence.remove-host-route',
        ),
    ]


def service_questions() -> list[dict]:
    records = read_jsonl("network/dhcp.jsonl")
    offer = next(record for record in records if record["message"] == "OFFER")
    sequence = " -> ".join(record["message"] for record in records)
    return [
        question(
            "services",
            "Enter the DHCP message sequence in order.",
            sequence,
            "The shared transaction follows Discover, Offer, Request, Acknowledge.",
            "network/dhcp.jsonl: records 1-4",
            ("dora",),
            question_id='m1.services.sequence',
        ),
        question(
            "services",
            "Which IPv4 address is offered to the client?",
            offer["address"],
            "The OFFER proposes the address later confirmed by the ACK.",
            "network/dhcp.jsonl: OFFER.address",
            question_id='m1.services.address',
        ),
        question(
            "services",
            "Which default gateway is supplied by DHCP?",
            offer["gateway"],
            "The gateway is configuration delivered to the host, not learned from DNS.",
            "network/dhcp.jsonl: OFFER.gateway",
            question_id='m1.services.gateway',
        ),
        question(
            "services",
            "Which DNS resolver is supplied by DHCP?",
            offer["dns"][0],
            "The resolver address is a DHCP option; DNS queries depend on it afterward.",
            "network/dhcp.jsonl: OFFER.dns[0]",
            question_id='m1.services.resolver',
        ),
    ]


def best_vrf_route(vrf: str, destination: str, tables: dict) -> dict | None:
    address = ipaddress.ip_address(destination)
    matches = [
        row for row in tables[vrf] if address in ipaddress.ip_network(row["prefix"])
    ]
    if not matches:
        return None
    return max(matches, key=lambda row: ipaddress.ip_network(row["prefix"]).prefixlen)


def vrf_questions() -> list[dict]:
    tables = read_json("routing/vrfs.json")
    cases = (
        ("CORP", "10.0.20.40"),
        ("CORP", "198.51.100.77"),
        ("MGMT", "10.0.30.50"),
        ("OT", "10.0.10.23"),
        ("OT", "10.0.40.10"),
    )
    result = []
    for vrf, destination in cases:
        route = best_vrf_route(vrf, destination, tables)
        reachable = route is not None
        detail = (
            f"{vrf} selects {route['prefix']} via {route['next_hop']}."
            if route
            else f"{vrf} contains no prefix matching {destination}."
        )
        result.append(
            question(
                "vrf",
                f"Does the {vrf} routing table contain a route for {destination}? (yes/no)",
                "yes" if reachable else "no",
                detail,
                f"routing/vrfs.json: .{vrf}",
                ("y",) if reachable else ("n",),
                question_id=f"m1.vrf.{vrf.lower()}.{destination}",
            )
        )
    return result


def troubleshooting_questions() -> list[dict]:
    traceroute = read_json("routing/traceroute.json")
    silent_hop = next(hop for hop in traceroute["hops"] if hop["response"] is None)
    later_response = next(
        hop for hop in traceroute["hops"] if hop["ttl"] > silent_hop["ttl"] and hop["response"]
    )
    return [
        question(
            "troubleshooting",
            "TCP connects, a 1400-byte payload is sent, ICMP reports MTU 1200, and the same payload is retransmitted. What is the leading diagnosis?",
            "path MTU mismatch",
            "Connectivity and the handshake work; the failure begins when the packet exceeds the reported path MTU.",
            "pcaps/mtu-failure.pcap: frames 1-6",
            ("mtu mismatch", "pmtu", "path mtu discovery failure"),
            question_id='m1.troubleshooting.transfer',
        ),
        question(
            "troubleshooting",
            f"Traceroute TTL {silent_hop['ttl']} is silent, but TTL {later_response['ttl']} reaches {later_response['response']}. Does the silence prove forwarding failed? (yes/no)",
            "no",
            traceroute["note"],
            "routing/traceroute.json: .hops and .note",
            ("n",),
            question_id='m1.troubleshooting.silent-hop',
        ),
        question(
            "troubleshooting",
            "Which capture is the healthy comparison: foundations.pcap or mtu-failure.pcap?",
            "foundations.pcap",
            "The foundations capture shows ARP, DNS, TCP, HTTP, and the start of orderly close; the final FIN acknowledgment is absent.",
            "pcaps/foundations.pcap",
            ("foundations",),
            question_id='m1.troubleshooting.healthy-capture',
        ),
        question(
            "troubleshooting",
            "What TCP MSS is advertised before the oversized payload is sent?",
            "1460",
            "Both SYN packets advertise MSS 1460 before the path reports MTU 1200.",
            "pcaps/mtu-failure.pcap: frames 1-2",
            question_id='m1.troubleshooting.mss',
        ),
    ]


def all_questions() -> dict[str, list[dict]]:
    return {
        "l2": l2_questions(),
        "routes": route_questions(),
        "convergence": convergence_questions(),
        "services": service_questions(),
        "vrf": vrf_questions(),
        "troubleshooting": troubleshooting_questions(),
    }


def choose_questions(activity: str, seed: int, limit: int | None) -> list[dict]:
    groups = all_questions()
    selected = sum(groups.values(), []) if activity == "all" else list(groups[activity])
    random.Random(seed).shuffle(selected)
    return selected[:limit] if limit else selected


def public_question(item: dict) -> dict:
    """Return a JSON-safe prompt without answers or a worked explanation."""
    return {key: item[key] for key in ("id", "activity", "prompt", "evidence")}


def evaluate_question(item: dict, response: str, *, revealed: bool = False) -> dict:
    """Evaluate a response without input, printing, or mutating the question."""
    if not isinstance(response, str):
        raise ValueError("answer must be text")
    evaluated = learning.evaluate(item, response)
    correct = not revealed and evaluated["correct"]
    result = dict(id=item["id"], correct=correct,
                  learning_result="revealed" if revealed else "correct" if correct else "incorrect",
                  feedback=item["explanation"] if correct or revealed else evaluated["feedback"])
    result.update(feedback_code=evaluated["feedback_code"], format_valid=evaluated["format_valid"])
    if revealed:
        result["answer"] = item["answer"]
    return result


def show_question(item: dict, number: int, reveal: bool) -> bool:
    print(f"\n{number}. [{item['activity']}] {item['prompt']}")
    print(f"   Evidence: labs/fixtures/{item['evidence']}")
    if reveal:
        correct = True
    else:
        correct = False
        attempts = 0
        while attempts < 2:
            try:
                response = input("   Your answer (? for help, show to reveal): ")
            except EOFError:
                raise SystemExit("\nerror: input ended before the activity was complete") from None
            if normalize(response) in {"?", "help"}:
                print("   Enter a short answer; capitalization is ignored.")
                continue
            if normalize(response) in {"s", "show"}:
                print("   Answer revealed.")
                break
            if evaluate_question(item, response)["correct"]:
                correct = True
                print("   Correct.")
                break
            attempts += 1
            if attempts < 2:
                print("   Not yet. Try once more or type show.")
            else:
                print(f"   Not yet. Expected: {item['answer']}")
    print(f"   Answer: {item['answer']}")
    print(f"   Why: {item['explanation']}")
    return correct


def run_session(activity: str, seed: int, limit: int | None, reveal: bool) -> int:
    selected = choose_questions(activity, seed, limit)
    label = "Demonstration" if reveal else "Practice"
    print(f"Module 1 Workbench — {label}")
    print(f"Seed: {seed} | Questions: {len(selected)}")
    score = sum(show_question(item, number, reveal) for number, item in enumerate(selected, 1))
    if not reveal:
        print(f"\nScore: {score}/{len(selected)}")
        print("Review each cited fixture before retrying with the same seed.")
    return 0


def practice_menu() -> int:
    activities = (("all", "mixed review"), *ACTIVITIES.items())
    print("Module 1 Practice")
    print("Choose a five-question session:")
    for number, (_, description) in enumerate(activities, 1):
        print(f"  {number}. {description}")
    while True:
        try:
            answer = input(f"Choose [1] (1-{len(activities)} or q): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not answer:
            answer = "1"
        if answer in {"q", "quit"}:
            return 0
        if answer.isdigit() and 1 <= int(answer) <= len(activities):
            return run_session(activities[int(answer) - 1][0], 1, 5, False)
        print(f"Enter 1-{len(activities)} or q.")


def verify_manifest() -> None:
    manifest = read_json("manifest.json")
    entries = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    for relative in (
        "network/l2-control.json",
        "network/dhcp.jsonl",
        "routing/route-candidates.csv",
        "routing/route-events.jsonl",
        "routing/traceroute.json",
        "routing/vrfs.json",
        "pcaps/foundations.pcap",
        "pcaps/mtu-failure.pcap",
    ):
        actual = hashlib.sha256((FIXTURES / relative).read_bytes()).hexdigest()
        assert entries[relative] == actual, f"fixture checksum mismatch: {relative}"


def self_test() -> int:
    verify_manifest()
    rows = route_rows()
    expected_routes = {
        "10.0.20.40": "10.0.20.40/32",
        "10.0.20.99": "10.0.20.0/24",
        "198.51.100.77": "198.51.100.77/32",
        "203.0.113.10": "0.0.0.0/0",
    }
    for destination, prefix in expected_routes.items():
        assert select_routes(destination, rows)[0]["prefix"] == prefix

    tables = read_json("routing/vrfs.json")
    assert best_vrf_route("OT", "10.0.10.23", tables) is None
    assert best_vrf_route("OT", "10.0.40.10", tables)["prefix"] == "10.0.40.0/24"
    assert best_vrf_route("CORP", "198.51.100.77", tables)["prefix"] == "0.0.0.0/0"

    groups = all_questions()
    ids = [item["id"] for items in groups.values() for item in items]
    assert len(ids) == len(set(ids)), "duplicate question IDs"
    assert set(groups) == set(ACTIVITIES)
    assert all(len(items) >= 4 for items in groups.values())
    assert groups["l2"][1]["answer"] == "sw-access-2"
    assert all(normalize(item["answer"]) in item["answers"] for items in groups.values() for item in items)
    print(f"self-test passed: {sum(map(len, groups.values()))} questions, 8 fixtures verified")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest="command", required=True)
    subcommands.add_parser("menu", help="choose a short guided practice session")
    subcommands.add_parser("list", help="list available activities")
    subcommands.add_parser("self-test", help="verify fixtures and workbench logic")
    for name, help_text in (("demo", "reveal worked answers"), ("run", "start scored practice")):
        command = subcommands.add_parser(name, help=help_text)
        command.add_argument("activity", nargs="?", choices=("all", *ACTIVITIES), default="all")
        command.add_argument("--seed", type=int, default=1, help="reproducible question order")
        command.add_argument("--limit", type=int, help="maximum number of questions")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "menu":
        return practice_menu()
    if args.command == "list":
        print("Module 1 Workbench activities:")
        for name, description in ACTIVITIES.items():
            print(f"  {name:15} {description}")
        return 0
    if args.command == "self-test":
        return self_test()
    if args.limit is not None and args.limit < 1:
        raise SystemExit("error: --limit must be at least 1")
    return run_session(args.activity, args.seed, args.limit, args.command == "demo")


if __name__ == "__main__":
    sys.exit(main())
