#!/usr/bin/env python3
"""Interactive, fixture-backed practice for Module 2."""

from __future__ import annotations

import argparse
import csv
import hashlib
import ipaddress
import json
import random
import sys
from pathlib import Path


ACTIVITIES = {
    "flows": "traffic paths, intended decisions, and policy points",
    "components": "routing, policy, state, transformation, and telemetry",
    "wan": "transport, path policy, and incomplete measurements",
    "cloud": "attachment route tables and longest-prefix selection",
    "failures": "failure conditions, scope, and blast radius",
}


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


def read_csv(relative: str) -> list[dict]:
    with (FIXTURES / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(line for line in handle if line.strip()))


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


def flow_questions() -> list[dict]:
    rows = read_csv("architecture/traffic-flows.csv")
    result = []
    for row in rows:
        description = (
            f"{row['source']} to {row['destination']} "
            f"{row['protocol']}/{row['port']}"
        )
        result.append(
            question(
                "flows",
                f"Which policy point evaluates flow {row['id']} ({description})?",
                row["policy_point"],
                f"Flow {row['id']} records {row['policy_point']} as its intended enforcement boundary.",
                f"architecture/traffic-flows.csv: row {row['id']}",
            )
        )
    for flow_id in ("F2", "F3", "F5"):
        row = next(item for item in rows if item["id"] == flow_id)
        result.append(
            question(
                "flows",
                f"Is flow {flow_id} intended to be allowed or denied?",
                row["intended"],
                f"The intended field is {row['intended']}; enforcement belongs at {row['policy_point']}.",
                f"architecture/traffic-flows.csv: row {flow_id}",
                ("allowed",) if row["intended"] == "allow" else ("denied",),
            )
        )
    return result


def component_questions() -> list[dict]:
    data = read_json("architecture/components.json")
    firewall = data["enterprise-firewall"]
    return [
        question(
            "components",
            "Which component routes, modifies, enforces policy, keeps state, but does not terminate TLS?",
            "enterprise-firewall",
            "Only the enterprise firewall has all four behaviors while tls_termination is false.",
            "architecture/components.json: .enterprise-firewall",
        ),
        question(
            "components",
            "Which component terminates TLS and creates backend traffic without routing packets?",
            "reverse-proxy",
            "The reverse proxy terminates TLS, modifies traffic, and keeps state while routes is false.",
            "architecture/components.json: .reverse-proxy",
        ),
        question(
            "components",
            "Which component reports alert and protocol telemetry without routing, modification, or policy enforcement?",
            "ids",
            "The IDS observes and records traffic; this model does not place it inline as an enforcer.",
            "architecture/components.json: .ids",
        ),
        question(
            "components",
            "Which TLS-terminating component also routes and reports backend health?",
            "load-balancer",
            "The load balancer has routes, tls_termination, and health telemetry set in its capability record.",
            "architecture/components.json: .load-balancer",
        ),
        question(
            "components",
            "Does the modeled enterprise firewall terminate TLS? (yes/no)",
            "no" if not firewall["tls_termination"] else "yes",
            "Its tls_termination field is false; session and NAT visibility do not imply payload decryption.",
            "architecture/components.json: .enterprise-firewall.tls_termination",
            ("n",) if not firewall["tls_termination"] else ("y",),
        ),
    ]


def wan_questions() -> list[dict]:
    data = read_json("architecture/wan.json")
    circuits = {item["name"]: item for item in data["circuits"]}
    degraded = next(item for item in data["circuits"] if item["state"] == "degraded")
    encrypted = next(item for item in data["circuits"] if item.get("encrypted"))
    preferred = min(data["circuits"], key=lambda item: item["preference"])
    loss_complete = all("loss_percent" in item for item in data["circuits"])
    return [
        question(
            "wan",
            "Which WAN circuit is degraded rather than down?",
            degraded["name"],
            f"Its state is degraded and its measured loss is {degraded['loss_percent']} percent.",
            "architecture/wan.json: .circuits",
        ),
        question(
            "wan",
            "Which circuit is explicitly marked encrypted?",
            encrypted["name"],
            "The internet VPN record explicitly sets encrypted to true.",
            "architecture/wan.json: .circuits",
        ),
        question(
            "wan",
            "Which circuit has the numerically lower configured preference?",
            preferred["name"],
            f"{preferred['name']} has preference {preferred['preference']}; lower is a recorded value, not proof of present usability.",
            "architecture/wan.json: .circuits[].preference",
        ),
        question(
            "wan",
            "What SD-WAN rule is recorded for business traffic?",
            data["sdwan_policy"]["business"],
            "The policy prefers private transport for the business class.",
            "architecture/wan.json: .sdwan_policy.business",
        ),
        question(
            "wan",
            "What SD-WAN rule is recorded for voice traffic?",
            data["sdwan_policy"]["voice"],
            "The policy states a selection objective; measurements are still needed to choose a circuit.",
            "architecture/wan.json: .sdwan_policy.voice",
        ),
        question(
            "wan",
            "Can this fixture prove which circuit currently has the lowest loss? (yes/no)",
            "yes" if loss_complete else "no",
            "internet-vpn-1 has no loss_percent field, so the two circuits cannot be compared from this fixture alone.",
            "architecture/wan.json: .circuits[].loss_percent",
            ("y",) if loss_complete else ("n",),
        ),
        question(
            "wan",
            "Does the modeled MPLS service provide encryption? (yes/no)",
            "yes" if data["mpls"]["encrypted"] else "no",
            "The model explicitly records encrypted as false; private transport is not the same as encryption.",
            "architecture/wan.json: .mpls.encrypted",
            ("y",) if data["mpls"]["encrypted"] else ("n",),
        ),
    ]


def cloud_route(attachment: str, destination: str, data: dict) -> tuple[str, dict | None]:
    table = data["attachments"][attachment]
    address = ipaddress.ip_address(destination)
    matches = [
        route for route in data["routes"][table] if address in ipaddress.ip_network(route["prefix"])
    ]
    if not matches:
        return table, None
    return table, max(matches, key=lambda route: ipaddress.ip_network(route["prefix"]).prefixlen)


def cloud_questions() -> list[dict]:
    data = read_json("architecture/cloud-routes.json")
    cases = (
        ("corp-vpc", "10.0.20.40"),
        ("corp-vpc", "8.8.8.8"),
        ("security-vpc", "10.20.5.10"),
        ("security-vpc", "8.8.8.8"),
        ("on-prem", "10.20.5.10"),
        ("on-prem", "8.8.8.8"),
    )
    result = []
    for attachment, destination in cases:
        table, route = cloud_route(attachment, destination, data)
        target = route["target"] if route else "no route"
        detail = (
            f"{attachment} uses {table}; prefix {route['prefix']} selects target {target}."
            if route
            else f"{attachment} uses {table}, which contains no matching prefix for {destination}."
        )
        result.append(
            question(
                "cloud",
                f"From attachment {attachment}, which target is selected for {destination}?",
                target,
                detail,
                f"architecture/cloud-routes.json: .attachments.{attachment} and .routes.{table}",
                ("none",) if route is None else (),
            )
        )
    return result


def failure_questions() -> list[dict]:
    records = read_jsonl("architecture/failures.jsonl")
    result = []
    for record in records:
        affected = ", ".join(record["affected"])
        result.append(
            question(
                "failures",
                f"What scope is affected when {record['component']} experiences {record['condition']}?",
                affected,
                f"The modeled event limits its affected scope to {affected}; broader impact would be an unsupported inference.",
                f"architecture/failures.jsonl: {record['component']} event",
            )
        )
    return result


def all_questions() -> dict[str, list[dict]]:
    return {
        "flows": flow_questions(),
        "components": component_questions(),
        "wan": wan_questions(),
        "cloud": cloud_questions(),
        "failures": failure_questions(),
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
        correct = False
        attempts = 0
        while attempts < 2:
            try:
                response = input("   Your answer (? for help, show to reveal): ")
            except EOFError:
                raise SystemExit("\nerror: input ended before the activity was complete") from None
            response = normalize(response)
            if response in {"?", "help"}:
                print("   Enter a short answer; capitalization is ignored.")
                continue
            if response in {"s", "show"}:
                print("   Answer revealed.")
                break
            if response in item["answers"]:
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
    print(f"Module 2 Workbench — {label}")
    print(f"Seed: {seed} | Questions: {len(selected)}")
    score = sum(show_question(item, number, reveal) for number, item in enumerate(selected, 1))
    if not reveal:
        print(f"\nScore: {score}/{len(selected)}")
        print("Review each cited fixture before retrying with the same seed.")
    return 0


def practice_menu() -> int:
    activities = (("all", "mixed review"), *ACTIVITIES.items())
    print("Module 2 Practice")
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
        "architecture/traffic-flows.csv",
        "architecture/components.json",
        "architecture/wan.json",
        "architecture/cloud-routes.json",
        "architecture/failures.jsonl",
    ):
        actual = hashlib.sha256((FIXTURES / relative).read_bytes()).hexdigest()
        assert entries[relative] == actual, f"fixture checksum mismatch: {relative}"


def self_test() -> int:
    verify_manifest()

    flows = {row["id"]: row for row in read_csv("architecture/traffic-flows.csv")}
    assert flows["F1"]["policy_point"] == "core-acl"
    assert flows["F4"]["intended"] == "deny"

    components = read_json("architecture/components.json")
    assert components["reverse-proxy"]["tls_termination"] is True
    assert components["ids"]["policy"] is False

    wan = read_json("architecture/wan.json")
    assert wan["circuits"][0]["state"] == "degraded"
    assert "loss_percent" not in wan["circuits"][1]

    cloud = read_json("architecture/cloud-routes.json")
    assert cloud_route("corp-vpc", "10.0.20.40", cloud)[1]["target"] == "on-prem"
    assert cloud_route("corp-vpc", "8.8.8.8", cloud)[1]["target"] == "security-vpc"
    assert cloud_route("on-prem", "8.8.8.8", cloud)[1] is None

    groups = all_questions()
    assert set(groups) == set(ACTIVITIES)
    assert all(len(items) >= 4 for items in groups.values())
    assert all(normalize(item["answer"]) in item["answers"] for items in groups.values() for item in items)
    print(f"self-test passed: {sum(map(len, groups.values()))} questions, 5 fixtures verified")
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
        print("Module 2 Workbench activities:")
        for name, description in ACTIVITIES.items():
            print(f"  {name:12} {description}")
        return 0
    if args.command == "self-test":
        return self_test()
    if args.limit is not None and args.limit < 1:
        raise SystemExit("error: --limit must be at least 1")
    return run_session(args.activity, args.seed, args.limit, args.command == "demo")


if __name__ == "__main__":
    sys.exit(main())
