"""Local, deterministic delivery of the six-hour Network Bootcamp."""

from __future__ import annotations

import argparse
import contextlib
import copy
import fcntl
import functools
import hashlib
import importlib.util
import itertools
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFINITION = "delivery/course.json"
ID = re.compile(r"[a-z0-9][a-z0-9.-]{0,79}\Z")
MARKER = re.compile(r"<!-- delivery:(start|end) ([a-z0-9.-]+) -->\Z")


class DeliveryError(Exception):
    def __init__(self, message: str, code: int = 2):
        super().__init__(message)
        self.code = code


def confined(base: Path, relative: str) -> Path:
    """Resolve only relative paths that remain inside the given directory."""
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise DeliveryError("Expected a relative path")
    path = base / relative
    if ".." in Path(relative).parts or not path.resolve().is_relative_to(base.resolve()):
        raise DeliveryError("Path escapes its directory")
    return path


def fragments(path: Path) -> dict[str, str]:
    result = {}
    active = None
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        marker = MARKER.fullmatch(line)
        if not marker:
            if "<!-- delivery:" in line:
                raise DeliveryError(f"Malformed delivery marker in {path.name}")
            if active:
                lines.append(line)
            continue
        action, name = marker.groups()
        if action == "start":
            if active or name in result:
                raise DeliveryError(f"Overlapping or duplicate fragment: {name}")
            active, lines = name, []
        else:
            if name != active:
                raise DeliveryError(f"Unmatched fragment end: {name}")
            result[name] = "\n".join(lines).strip()
            active = None
    if active:
        raise DeliveryError(f"Unclosed fragment: {active}")
    return result


def read_fragment(reference: dict) -> str:
    path = confined(ROOT, reference["path"])
    content = fragments(path)
    if reference["fragment"] not in content:
        raise DeliveryError(f"Missing fragment: {reference['fragment']}")
    return content[reference["fragment"]]


def definition() -> dict:
    try:
        data = json.loads((ROOT / DEFINITION).read_text(encoding="utf-8"))
        validate_definition(data)
        return data
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise DeliveryError(f"Invalid delivery definition: {error}") from error


def validate_definition(data: dict) -> None:
    if data["schema_version"] != 1 or not data["course_version"]:
        raise DeliveryError("Unsupported course definition version")
    blocks = data["blocks"]
    if [block["id"] for block in blocks] != ["opening", "c01", "c02", "c03", "c04", "c05", "c06", "exit"]:
        raise DeliveryError("Expected opening, six challenges, and exit")
    minutes = [block["minutes"] for block in blocks]
    if minutes != [15, 65, 45, 40, 60, 65, 55, 15]:
        raise DeliveryError("Teaching schedule must total the agreed 360 minutes")
    if [block["break_after"] for block in blocks] != [0, 15, 0, 30, 0, 15, 0, 0]:
        raise DeliveryError("Break schedule must preserve 15/30/15 minutes")
    agenda = (ROOT / "agenda.md").read_text(encoding="utf-8")
    agenda_minutes = [int(value) for value in re.findall(r"^\| \d\d:\d\d–\d\d:\d\d \| (\d+) \|", agenda, re.M)]
    if agenda_minutes != minutes:
        raise DeliveryError("Delivery schedule differs from agenda.md")
    seen = set()
    totals = dict.fromkeys([block["id"] for block in blocks], 0)
    previous = None
    for phase in data["phases"]:
        name = phase["id"]
        if not ID.fullmatch(name) or name in seen:
            raise DeliveryError(f"Invalid or duplicate phase: {name}")
        if phase["prerequisites"] != ([previous] if previous else []):
            raise DeliveryError(f"Invalid order or cyclic dependency: {name}")
        if phase["block"] not in totals or type(phase["minutes"]) is not int or phase["minutes"] <= 0:
            raise DeliveryError(f"Invalid block or duration: {name}")
        if phase["kind"] not in {"prediction", "reflection", "checkpoint", "review", "feedback"}:
            raise DeliveryError(f"Unknown phase kind: {name}")
        if phase["implemented"]:
            if not phase["content"]:
                raise DeliveryError(f"Missing teaching content: {name}")
            for reference in phase["content"] + phase["hints"] + phase["solutions"]:
                for case in ("A", "B"):
                    read_fragment(resolve_reference(reference, {"case": case}))
            if any(view not in EVIDENCE for view in phase["evidence"]):
                raise DeliveryError(f"Unknown evidence view: {name}")
            if any(check not in checkpoint_ids() for check in phase["checkpoints"]):
                raise DeliveryError(f"Unknown checkpoint: {name}")
        totals[phase["block"]] += phase["minutes"]
        seen.add(name)
        previous = name
    if list(totals.values()) != minutes:
        raise DeliveryError("Phase durations differ from block durations")


EVIDENCE = {
    "transfer.summary": ["tshark", "-r", "labs/fixtures/challenges/transfer.pcap"],
    "transfer.fields": ["tshark", "-r", "labs/fixtures/challenges/transfer.pcap", "-Y", "tcp || icmp", "-T", "fields", "-E", "header=y", "-e", "frame.number", "-e", "frame.time_relative", "-e", "ip.src", "-e", "ip.dst", "-e", "ip.len", "-e", "ip.hdr_len", "-e", "tcp.hdr_len", "-e", "tcp.len", "-e", "tcp.seq", "-e", "tcp.options.mss_val", "-e", "icmp.type", "-e", "icmp.code", "-e", "icmp.mtu"],
    "transfer.icmp": ["tshark", "-r", "labs/fixtures/challenges/transfer.pcap", "-Y", "icmp", "-V"],
}
EVIDENCE.update({
    'dhcp': ['jq', '.', 'labs/fixtures/network/dhcp.jsonl'],
    'foundations.summary': ['tshark', '-r', 'labs/fixtures/pcaps/foundations.pcap'],
    'foundations.fields': ['tshark', '-r', 'labs/fixtures/pcaps/foundations.pcap', '-T', 'fields', '-E', 'header=y', '-e', 'frame.number', '-e', 'vlan.id', '-e', 'eth.src', '-e', 'eth.dst', '-e', 'ip.src', '-e', 'ip.dst', '-e', 'tcp.flags', '-e', 'dns.qry.name', '-e', 'http.response.code'],
    'routes': ['column', '-s,', '-t', 'labs/fixtures/routing/route-candidates.csv'],
    'ospf': ['jq', '.', 'labs/fixtures/routing/ospf.json'],
    'route-events': ['jq', '-c', '.', 'labs/fixtures/routing/route-events.jsonl'],
    'bgp': ['jq', '.', 'labs/fixtures/routing/bgp.json'],
    'vrfs': ['jq', '.', 'labs/fixtures/routing/vrfs.json'],
    'enterprise': ['cat', 'labs/fixtures/architecture/enterprise.md'],
    'components': ['jq', '.', 'labs/fixtures/architecture/components.json'],
    'flows': ['column', '-s,', '-t', 'labs/fixtures/architecture/traffic-flows.csv'],
    'cloud': ['jq', '.', 'labs/fixtures/architecture/cloud-routes.json'],
    'wan': ['jq', '.', 'labs/fixtures/architecture/wan.json'],
    'failures.hidden': ['jq', '-c', 'del(.affected)', 'labs/fixtures/architecture/failures.jsonl'],
    'failures.outcomes': ['jq', '-c', '{component, affected}', 'labs/fixtures/architecture/failures.jsonl'],
    'incident.round1': ['jq', '.', 'labs/fixtures/challenges/incident-round-1.json'],
    'incident.round2': ['jq', '.', 'labs/fixtures/challenges/incident-round-2.json'],
    'incident.round3': ['jq', '.', 'labs/fixtures/challenges/incident-round-3.json'],
    'incident.packets': ['tshark', '-r', 'labs/fixtures/pcaps/incident.pcap', '-Y', 'dns || tls.handshake.type == 1', '-T', 'fields', '-E', 'header=y', '-e', 'frame.number', '-e', 'ip.src', '-e', 'ip.dst', '-e', 'dns.qry.name', '-e', 'tls.handshake.extensions_server_name'],
    'case.main': ['jq', '.', 'labs/fixtures/challenges/case-a.json'],
    'case.exit': ['jq', '.', 'labs/fixtures/challenges/case-b.json'],
    "incident.timeline": [sys.executable, "-B", "course.py", "timeline"],
})
CHECKPOINTS = {
    "opening.local", "opening.dns", "opening.application", "transfer.payload",
    "route.before-hops", "route.after-hops", "routing.bgp-peer", "routing.corp-route",
    "routing.ot-route", "flows.server-ot", "flows.user-ot", "budget.options",
    "incident.utc", "incident.auth-record", "case.id", "case.change", "case.lookup",
    "case.observation",
}

WORK_ROOT = ROOT / "work"
SESSION_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,47}\Z")
ARTIFACTS = {
    "packet-path.md": "challenges/templates/packet-path.md",
    "architecture.md": "challenges/templates/architecture.md",
    "incident.md": "challenges/templates/incident.md",
    "evidence-ledger.csv": "labs/fixtures/incident/evidence-ledger-template.csv",
}
DIMENSIONS = ("mechanism", "evidence", "uncertainty", "action")
OUTPUT_LIMIT = 65536
STATE_LIMIT = 32 * 1024 * 1024


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def decode_json(text: str):
    def invalid(value):
        raise ValueError(f"Non-finite JSON number: {value}")
    try:
        return json.loads(text, parse_constant=invalid)
    except (ValueError, TypeError) as error:
        raise DeliveryError(f"Invalid JSON: {error}") from error


def module_at(relative: str):
    path = confined(ROOT, relative)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@functools.lru_cache(maxsize=3)
def workbench(number: int):
    path = next(ROOT.glob(f"modules/*/workbench/module{number}_workbench.py"))
    return module_at(str(path.relative_to(ROOT)))


def checkpoint_ids() -> set[str]:
    return CHECKPOINTS | {item["id"] for number in (1, 2, 3)
                          for group in workbench(number).all_questions().values() for item in group}


def evidence_integrity() -> None:
    try:
        manifest = decode_json((ROOT / "labs/fixtures/manifest.json").read_text())
        for entry in manifest["files"]:
            confined(ROOT / "labs/fixtures", entry["path"])
        errors = module_at("labs/build_fixtures.py").check()
        if errors:
            raise DeliveryError("; ".join(errors), 4)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise DeliveryError(f"Cannot verify evidence: {error}. Restore the matching course files.", 4) from error


def versions(data: dict) -> dict:
    paths = {DEFINITION, "delivery.py", "course.py", "agenda.md", *ARTIFACTS.values()}
    paths.update(str(path.relative_to(ROOT)) for path in ROOT.glob("modules/*/workbench/*.py"))
    for phase in data["phases"]:
        for reference in phase["content"] + phase["hints"] + phase["solutions"]:
            paths.add(reference["path"])
    digest = hashlib.sha256()
    for relative in sorted(paths):
        digest.update(relative.encode() + b"\0" + confined(ROOT, relative).read_bytes() + b"\0")
    return {
        "course": data["course_version"],
        "content_sha256": digest.hexdigest(),
        "fixtures_sha256": hashlib.sha256((ROOT / "labs/fixtures/manifest.json").read_bytes()).hexdigest(),
    }


def run_tool(argv: list[str], timeout: float = 15) -> dict:
    """Bound memory use even when a broken local tool emits excessive output."""
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        timed_out = False
        try:
            process = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL,
                                     stdout=stdout, stderr=stderr, timeout=timeout, check=False)
            returncode = process.returncode
        except FileNotFoundError:
            raise DeliveryError(f"Missing tool {argv[0]}; run ./prerequisites/setup.sh", 4) from None
        except subprocess.TimeoutExpired:
            timed_out, returncode = True, None
        stdout.seek(0)
        stderr.seek(0)
        out, err = stdout.read(OUTPUT_LIMIT + 1), stderr.read(OUTPUT_LIMIT + 1)
    return dict(command=shlex.join(argv), returncode=returncode, timed_out=timed_out,
                stdout=out[:OUTPUT_LIMIT].decode("utf-8", errors="replace"),
                stderr=err[:OUTPUT_LIMIT].decode("utf-8", errors="replace"),
                truncated=len(out) > OUTPUT_LIMIT or len(err) > OUTPUT_LIMIT)


def evidence_command(view: str, state: dict) -> list[str]:
    command = list(EVIDENCE[view])
    if view in {"case.main", "case.exit"}:
        letter = state["case"] if view == "case.main" else other_case(state)
        command[-1] = f"labs/fixtures/challenges/case-{letter.lower()}.json"
    return command


def other_case(state: dict) -> str:
    return "B" if state["case"] == "A" else "A"


def resolve_reference(reference: dict, state: dict) -> dict:
    return {**reference, "fragment": reference["fragment"].replace("{main}", state["case"].lower()).replace("{exit}", other_case(state).lower())}


def doctor() -> dict:
    checks = []
    def check(name, operation):
        try:
            detail = operation()
            checks.append(dict(name=name, ready=True, detail=detail))
        except (DeliveryError, OSError) as error:
            checks.append(dict(name=name, ready=False, detail=str(error)))
    def require(value, message):
        if not value:
            raise DeliveryError(message, 4)
        return str(value)
    check("macOS", lambda: require(platform.system() == "Darwin", "Supported delivery requires macOS"))
    check("Python", lambda: require(sys.version_info >= (3, 10), "Python 3.10 or later is required") and platform.python_version())
    check("fixtures", lambda: evidence_integrity() or "Manifest and evidence verified")
    check("definition", lambda: definition()["course_version"])
    for command in ("tshark", "jq", "column"):
        check(command, lambda command=command: require(shutil.which(command), f"Missing {command}; run ./prerequisites/setup.sh"))
    def capability(argv, expected):
        result = run_tool(argv)
        if result["returncode"] != 0 or result["truncated"] or expected not in result["stdout"]:
            raise DeliveryError(f"Capability failed: {shlex.join(argv)}. Check the installed tool version.", 4)
        return "Capability check passed"
    check("jq capability", lambda: capability(["jq", "-n", "{ready: true}.ready"], "true"))
    check("TShark fields", lambda: capability(EVIDENCE["transfer.fields"], "1200"))
    tool_versions = {}
    for name in ("jq", "tshark"):
        if shutil.which(name):
            try:
                tool_versions[name] = run_tool([name, "--version"])["stdout"].splitlines()[:1]
            except DeliveryError as error:
                tool_versions[name] = [str(error)]
    return dict(ready=all(item["ready"] for item in checks), checks=checks,
                versions=tool_versions,
                extended={name: bool(shutil.which(name)) for name in ("zeek", "iperf3")},
                optional_live={name: bool(shutil.which(name)) for name in ("tcpdump", "netstat", "route", "arp", "traceroute", "nc")})


def session_dir(ident: str) -> Path:
    if not isinstance(ident, str) or not SESSION_ID.fullmatch(ident):
        raise DeliveryError("Session ID must be 1–48 lowercase letters, digits, or hyphens")
    if WORK_ROOT.is_symlink():
        raise DeliveryError("The work directory must not be a symlink")
    path = confined(WORK_ROOT, ident)
    if path.is_symlink():
        raise DeliveryError("Session directories must not be symlinks")
    return path


def session_file(directory: Path, name: str) -> Path:
    path = confined(directory, name)
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent.is_relative_to(directory)):
        raise DeliveryError("Session files must not be symlinks")
    return path


def save_state(directory: Path, state: dict) -> None:
    raw = json.dumps(state, ensure_ascii=False, allow_nan=False).encode("utf-8")
    # ponytail: one bounded JSON file per six-hour session; archive and start a
    # new session if an unusually long practice history reaches this ceiling.
    if len(raw) > STATE_LIMIT:
        raise DeliveryError("Session history is full; export it before starting a new session", 4)
    destination = session_file(directory, "session.json")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=directory, prefix=".session-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


@contextlib.contextmanager
def session_lock(directory: Path):
    if not directory.is_dir():
        raise DeliveryError("Session not found; create it first", 3)
    with session_file(directory, ".lock").open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise DeliveryError("Another request is updating this session; retry", 3) from None
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def load_state(directory: Path, data: dict) -> dict:
    try:
        path = session_file(directory, "session.json")
        if path.stat().st_size > STATE_LIMIT:
            raise ValueError("state exceeds size limit")
        state = decode_json(path.read_text(encoding="utf-8"))
        order = [phase["id"] for phase in data["phases"] if phase["implemented"]]
        if (state["schema_version"] != 1 or state["id"] != directory.name
                or state["order"] != order or type(state["revision"]) is not int
                or state["revision"] < 0 or state["case"] not in ("A", "B")
                or not isinstance(state["requests"], dict)
                or not isinstance(state["phases"], dict)
                or state["current"] not in [None, *order]):
            raise ValueError("invalid session fields")
        for name in order:
            progress = state["phases"][name]
            if not isinstance(progress["submissions"], list) or not isinstance(progress["checks"], dict):
                raise ValueError("invalid phase history")
    except (OSError, ValueError, KeyError, TypeError, DeliveryError) as error:
        raise DeliveryError(f"Cannot load session: {error}. Preserve this directory; restore a saved copy or create a new session.", 3) from error
    if state["versions"] != versions(data):
        raise DeliveryError("Course or fixture version changed. Use the matching course copy or create a new session; existing work was preserved.", 3)
    evidence_integrity()
    return state


def create_session(ident: str, mode: str = "solo", case: str = "A", pair_label: str | None = None, seed: int = 1) -> dict:
    data = definition()
    directory = session_dir(ident)
    if mode not in ("solo", "pair") or case not in ("A", "B") or type(seed) is not int:
        raise DeliveryError("Invalid delivery mode, case, or seed")
    if pair_label is not None and (mode != "pair" or not SESSION_ID.fullmatch(pair_label)):
        raise DeliveryError("Use an anonymous pair label with pair mode")
    if directory.exists():
        raise DeliveryError("Session already exists; use status or learn to resume", 3)
    readiness = doctor()
    if not readiness["ready"]:
        failures = "; ".join(item["detail"] for item in readiness["checks"] if not item["ready"])
        raise DeliveryError(f"Course is not ready: {failures}. Run ./course doctor --json for details.", 4)
    order = [phase["id"] for phase in data["phases"] if phase["implemented"]]
    if not order:
        raise DeliveryError("No phases are implemented", 4)
    state = dict(schema_version=1, id=ident, versions=versions(data), mode=mode,
                 pair_label=pair_label, case=case, seed=seed,
                 question_ids={str(n): [item["id"] for item in workbench(n).choose_questions("all", seed, 5)] for n in (1, 2, 3)},
                 revision=0, created_at=now(), updated_at=now(), order=order,
                 current=order[0], requests={}, phases={})
    for name in order:
        state["phases"][name] = dict(status="incomplete", submissions=[], checks={},
                                     views=[], hints=0, exposed=False, reviews=[])
    directory.parent.mkdir(parents=True, exist_ok=True)
    try:
        directory.mkdir()
    except FileExistsError:
        raise DeliveryError("Session already exists; resume it instead", 3) from None
    for name, source in ARTIFACTS.items():
        with session_file(directory, name).open("xb") as handle:
            handle.write((ROOT / source).read_bytes())
    save_state(directory, state)
    return status_result(state, data)


def phase_by_id(data: dict, name: str) -> dict:
    for phase in data["phases"]:
        if phase["id"] == name:
            return phase
    raise DeliveryError(f"Unknown phase: {name}")


def checkpoint_items(phase: dict, state: dict) -> list[dict]:
    items = {
        "transfer.payload": dict(id="transfer.payload", prompt="Largest TCP payload with MTU 1200, 20-byte IPv4 and TCP headers, no options or encapsulation? Include units.",
                                 evidence="challenges/transfer.pcap: frames 4–6",
                                 explanation="1200 minus the two 20-byte headers leaves 1160 payload bytes.",
                                 answer="1160 bytes", answers={"1160 bytes", "1160 byte", "1160 b"}),
    }
    def add(name, prompt, answer, evidence, aliases=()):
        items[name] = workbench(1).question("delivery", prompt, answer,
            f"Compare this answer with {evidence}; your explanation still requires review.",
            evidence, aliases, question_id=name)
    requested = set(phase["checkpoints"])
    if any(name.startswith("opening.") for name in requested):
        add("opening.local", "Is 10.0.10.53 local to 10.0.10.23/24? (yes/no)", "yes", "opening diagnostic: /24 subnet", ("y",))
        add("opening.dns", "Does resolving a name prove the server is reachable? (yes/no)", "no", "opening diagnostic: DNS dependency", ("n",))
        add("opening.application", "Does a completed TCP handshake prove application success? (yes/no)", "no", "opening diagnostic: transport boundary", ("n",))
    if any(name.startswith("route.") for name in requested):
        rows = workbench(1).route_rows()
        for stage, candidates in (("before", rows), ("after", [r for r in rows if r["prefix"] != "10.0.20.40/32"])):
            hops = sorted({r["next_hop"] for r in workbench(1).select_routes("10.0.20.40", candidates)})
            add(f"route.{stage}-hops", f"List every eligible next hop for 10.0.20.40 {stage} removing its /32 route; separate IPs with commas.",
                ", ".join(hops), "routing/route-candidates.csv", tuple(", ".join(order) for order in itertools.permutations(hops)))
    if any(name.startswith("routing.") for name in requested):
        bgp = workbench(1).read_json("routing/bgp.json")
        candidates = [r for r in bgp["routes"] if r["accepted"] and r["prefix"] == "198.51.100.0/24"]
        peer = max(candidates, key=lambda r: r["local_pref"])["peer"]
        add("routing.bgp-peer", "Which accepted peer wins for 198.51.100.0/24 under the supplied BGP attributes?", peer, "routing/bgp.json")
        tables = workbench(1).read_json("routing/vrfs.json")
        for context in ("CORP", "OT"):
            route = workbench(1).best_vrf_route(context, "198.51.100.77", tables)
            add(f"routing.{context.lower()}-route", f"What prefix matches 198.51.100.77 in {context}, or 'no route'?",
                route["prefix"] if route else "no route", f"routing/vrfs.json: {context}", ("none",) if not route else ())
    if any(name.startswith("flows.") for name in requested):
        flows = {r["id"]: r for r in workbench(2).read_csv("architecture/traffic-flows.csv")}
        for name, flow in (("server-ot", "F3"), ("user-ot", "F4")):
            answer = flows[flow]["intended"]
            add(f"flows.{name}", f"What is the intended decision for {flow}: allow or deny?", answer, f"architecture/traffic-flows.csv: {flow}", ("allowed" if answer == "allow" else "denied",))
    if "budget.options" in requested:
        options = ("state-sync", "backup-path", "monitoring", "management")
        pairs = [", ".join(pair) for pair in itertools.permutations(options, 2)]
        add("budget.options", "Choose exactly two different option IDs: state-sync, backup-path, monitoring, management. Explain the tradeoff in your text.",
            pairs[0], "Challenge 4: two-token table", tuple(pairs))
        items["budget.options"]["explanation"] = "Two valid choices recorded. Their merits and residual risk require rubric review."
        items["budget.options"]["answer"] = "Any two distinct option IDs; no pair satisfies every requirement."
    if "incident.utc" in requested:
        timestamp = workbench(3).parse_time("2026-08-15T10:04:01-06:00").astimezone(timezone.utc)
        add("incident.utc", "Normalize 2026-08-15T10:04:01-06:00 to UTC (YYYY-MM-DDTHH:MM:SSZ).", timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "incident/auth.jsonl", (timestamp.isoformat(), timestamp.strftime("%Y-%m-%dT%H:%M:%S.000Z")))
        records = workbench(3).read_jsonl("incident/auth.jsonl")
        record = next(i for i, r in enumerate(records, 1) if workbench(3).parse_time(r["time"]) == timestamp)
        add("incident.auth-record", "Which original authentication record has that timestamp? Enter its one-based record number.", str(record), "incident/auth.jsonl")
    if any(name.startswith("case.") for name in requested):
        letter = other_case(state) if phase["block"] == "exit" else state["case"]
        case = workbench(1).read_json(f"challenges/case-{letter.lower()}.json")
        evidence = f"challenges/case-{letter.lower()}.json"
        add("case.id", "Enter the exact ID of your assigned case.", case["case"], evidence)
        if letter == "A":
            missing = [r["prefix"] for r in case["before"]["routes"]["on-prem"] if r not in case["after"]["routes"]["on-prem"]]
            add("case.change", "What exact return-route prefix was removed?", missing[0], evidence + ": before/after on-prem")
            route = workbench(1).best_vrf_route("on-prem", case["flow"]["src"], case["after"]["routes"])
            prompt = "What prefix matches the returning reply's destination in on-prem after the change, or 'no route'?"
        else:
            add("case.change", "What ingress VRF became active after the change?", case["after"]["ingress_vrf"], evidence + ": after.ingress_vrf")
            route = workbench(1).best_vrf_route(case["after"]["ingress_vrf"], case["flow"]["dst"], case["routes"])
            prompt = "What prefix matches the outbound destination in the active VRF, or 'no route'?"
        add("case.lookup", prompt, route["prefix"] if route else "no route", evidence + ": routes", ("none",) if not route else ())
        record = next(r for r in case["observations"] if "no matching" in r["event"])
        add("case.observation", "Which observation ID directly records the failed route lookup?", record["id"], evidence + ": observations")
    for name in phase["checkpoints"]:
        if name.startswith(("m1.", "m2.", "m3.")):
            number = int(name[1])
            for group in workbench(number).all_questions().values():
                for item in group:
                    if item["id"] == name:
                        items[name] = {**item, "module": number}
    return [items[name] for name in phase["checkpoints"]]


def public_checkpoint(item: dict) -> dict:
    return {key: item[key] for key in ("id", "prompt", "evidence")}


def render_references(references: list[dict], state: dict) -> str:
    chunks = []
    for reference in references:
        text = read_fragment(resolve_reference(reference, state))
        if reference["fragment"] == "c06.receive":
            text = text.replace("Choose **A** for the team capstone; reserve **B** for the individual exit task.\nA facilitator may reverse them, but do not read the reserved case early.",
                                f"Your assigned main capstone is **{state['case']}**. Reserve the other case for the individual exit.")
            text = text.replace("case-a.json", f"case-{state['case'].lower()}.json")
        if reference["fragment"] == "exit.answer":
            text = text.replace("case-b.json", f"case-{other_case(state).lower()}.json")
            text = text.replace("If your group used B,\nuse A instead.", "")
        text = re.sub(r"\[([^\]]+)\]\([^)]*(?:facilitator/solutions|hints)\.md[^)]*\)", r"\1 (use the hint or reveal action)", text)
        chunks.append(text.replace("work/bootcamp", f"work/{state['id']}"))
    return "\n\n".join(chunks)


def allowed_actions(phase: dict) -> list[str]:
    actions = ["answer", "continue", "skip"]
    if phase["kind"] == "prediction":
        actions.insert(0, "predict")
    if phase["evidence"]:
        actions.append("evidence")
    if phase["hints"]:
        actions.append("hint")
    if phase["solutions"]:
        actions.append("reveal")
    if phase["kind"] == "review":
        actions.append("review")
    if phase["kind"] == "feedback":
        actions.append("feedback")
    if phase["id"] in ("c03.review", "c04.review", "c05.review"):
        actions.append("practice")
    return actions


def completion(state: dict, data: dict) -> dict:
    checked = [phase for phase in data["phases"] if phase["implemented"] and phase["checkpoints"]]
    objective = all(state["phases"][p["id"]]["checks"].get(name, {}).get("independent", False)
                    for p in checked for name in p["checkpoints"])
    required = all(value["status"] in ("complete", "pending_review") for value in state["phases"].values())
    finished = state["current"] is None and all(p["implemented"] for p in data["phases"])
    return dict(delivery_finished=finished, required_work_recorded=required,
                objective_checks_satisfied=objective, self_reviewed_completion=False,
                facilitator_reviewed_completion=False)


def status_result(state: dict, data: dict, result: dict | None = None, view_phase: str | None = None) -> dict:
    current = view_phase or state["current"]
    view = None
    if current:
        phase = phase_by_id(data, current)
        view = {key: phase[key] for key in ("id", "block", "kind", "minutes", "artifacts")}
        view.update(prompt=render_references(phase["content"], state),
                    checkpoints=[public_checkpoint(item) for item in checkpoint_items(phase, state)],
                    evidence=[dict(id=name, command=shlex.join(evidence_command(name, state))) for name in phase["evidence"]],
                    allowed_actions=allowed_actions(phase),
                    progress=copy.deepcopy(state["phases"][current]))
        block = next(b for b in data["blocks"] if b["id"] == phase["block"])
        view["block_title"] = block["title"]
        next_position = state["order"].index(current) + 1
        end_of_block = next_position == len(state["order"]) or phase_by_id(data, state["order"][next_position])["block"] != phase["block"]
        view["break_after_minutes"] = block["break_after"] if end_of_block else 0
        view["mode_prompt"] = "Write your own explanation before continuing." if state["mode"] == "solo" else "Swap evidence-reader and skeptical-reviewer roles; record your own answer. The exit is individual."
        if "practice" in view["allowed_actions"]:
            view["practice"] = [workbench(number).public_question(item) for number, item in practice_items(phase, state)]
    released = state["order"][:state["order"].index(state["current"]) + 1] if state["current"] else state["order"]
    return dict(protocol_version=1, status="ok", session_id=state["id"], revision=state["revision"],
                phase=view, completion=completion(state, data), result=result,
                current_phase_id=state["current"],
                released_phases=[dict(id=name, status=state["phases"][name]["status"]) for name in released],
                workspace=f"work/{state['id']}")


def session_status(ident: str, phase_id: str | None = None) -> dict:
    data = definition()
    state = load_state(session_dir(ident), data)
    if phase_id is not None:
        released = state["order"][:state["order"].index(state["current"]) + 1] if state["current"] else state["order"]
        if phase_id not in released:
            raise DeliveryError("This phase has not been released yet", 3)
    return status_result(state, data, view_phase=phase_id)


def practice_items(phase: dict, state: dict) -> list[tuple[int, dict]]:
    number = {"c03.review": 1, "c04.review": 2, "c05.review": 3}[phase["id"]]
    available = {item["id"]: item for group in workbench(number).all_questions().values() for item in group}
    return [(number, available[name]) for name in state["question_ids"][str(number)]]


def require_text(value, label="text") -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 16000:
        raise DeliveryError(f"{label} must be nonempty text of at most 16000 characters")
    return value.strip()


def artifact_hashes(directory: Path, names: list[str]) -> dict:
    return {name: hashlib.sha256(session_file(directory, name).read_bytes()).hexdigest() for name in names}


def act(ident: str, request: dict) -> dict:
    if not isinstance(request, dict) or set(request) != {"request_id", "expected_revision", "phase_id", "action", "payload"}:
        raise DeliveryError("Request needs request_id, expected_revision, phase_id, action, and payload")
    if (not isinstance(request["request_id"], str) or not ID.fullmatch(request["request_id"])
            or type(request["expected_revision"]) is not int or not isinstance(request["payload"], dict)):
        raise DeliveryError("Invalid request ID, revision, or payload")
    data = definition()
    directory = session_dir(ident)
    with session_lock(directory):
        state = load_state(directory, data)
        old = state["requests"].get(request["request_id"])
        if old:
            if old["request"] != request:
                raise DeliveryError("Request ID was already used for different input", 3)
            return old["response"]
        if state["revision"] != request["expected_revision"]:
            raise DeliveryError("Stale session revision; fetch status and retry with a new request ID", 3)
        name = request["phase_id"]
        if name not in state["order"]:
            raise DeliveryError("Unknown or unfinished phase")
        position = state["order"].index(name)
        current_position = state["order"].index(state["current"]) if state["current"] else len(state["order"])
        if position > current_position:
            raise DeliveryError("This phase has not been released yet", 3)
        phase = phase_by_id(data, name)
        progress = state["phases"][name]
        action, payload = request["action"], request["payload"]
        if action not in allowed_actions(phase):
            raise DeliveryError("Action is not available in this phase", 3)
        result = {"action": action, "phase_id": name}
        if action in ("answer", "predict"):
            text = require_text(payload.get("text"))
            items = checkpoint_items(phase, state)
            answers = payload.get("answers", {})
            if not isinstance(answers, dict) or set(answers) != {item["id"] for item in items}:
                raise DeliveryError("Supply exactly the checkpoint answer IDs shown in status")
            checks = {}
            for item in items:
                answer = require_text(answers[item["id"]], item["id"])
                evaluated = workbench(item.get("module", 1)).evaluate_question(item, answer)
                correct = evaluated["correct"]
                checks[item["id"]] = dict(correct=correct, independent=correct and not progress["exposed"],
                                          feedback="Correct." if correct else f"Reinspect {item['evidence']} and try again; include requested units.")
            progress["checks"] = checks
            progress["submissions"].append(dict(at=now(), text=text, answers=answers, checks=copy.deepcopy(checks)))
            progress["status"] = "incomplete"
            result.update(learning_result="incorrect" if any(not c["correct"] for c in checks.values()) else "recorded", checks=checks)
        elif action == "evidence":
            view = payload.get("view")
            if view not in phase["evidence"]:
                raise DeliveryError("Evidence view is not available in this phase", 3)
            output = run_tool(evidence_command(view, state))
            if output["returncode"] != 0 or output["truncated"]:
                raise DeliveryError(f"Evidence command failed or exceeded limits; phase unchanged: {output}", 4)
            if view not in progress["views"]:
                progress["views"].append(view)
            result.update(view=view, output=output, fixture_manifest_sha256=state["versions"]["fixtures_sha256"])
        elif action == "hint":
            index = progress["hints"]
            result["text"] = render_references(phase["hints"][index:index + 1], state) if index < len(phase["hints"]) else "No further hints; revise your response or request a worked reveal."
            progress["hints"] = min(index + 1, len(phase["hints"]))
        elif action == "reveal":
            result["text"] = render_references(phase["solutions"], state)
            result["answers"] = {item["id"]: item["answer"] for item in checkpoint_items(phase, state)}
            for peer in data["phases"]:
                if peer["block"] == phase["block"] and peer["id"] in state["phases"]:
                    prior = state["phases"][peer["id"]]
                    if not prior["checks"] or not all(c["correct"] for c in prior["checks"].values()):
                        prior["exposed"] = True
            result["learning_result"] = "revealed"
        elif action == "review":
            scores = payload.get("scores")
            if (payload.get("reviewer") not in ("self", "facilitator") or not isinstance(scores, dict)
                    or set(scores) != set(DIMENSIONS) or any(type(v) is not int or not 0 <= v <= 2 for v in scores.values())):
                raise DeliveryError("Review needs reviewer self/facilitator and four integer scores from 0 to 2")
            review = dict(at=now(), reviewer=payload["reviewer"], scores=scores,
                          feedback=require_text(payload.get("feedback"), "feedback"),
                          artifact_hashes=artifact_hashes(directory, phase["artifacts"]))
            review["passed"] = sum(scores.values()) >= 6 and min(scores.values()) > 0
            progress["reviews"].append(review)
            result["learning_result"] = "reviewed" if review["passed"] else "needs_revision"
        elif action == "feedback":
            for key in ("wanted_to_know", "manageable"):
                if payload.get(key) is not None and (type(payload[key]) is not int or not 1 <= payload[key] <= 5):
                    raise DeliveryError("Optional engagement ratings must be integers from 1 to 5")
            progress["feedback"] = {key: payload.get(key) for key in ("wanted_to_know", "manageable")}
            if "text" in payload:
                progress["feedback"]["text"] = require_text(payload["text"])
            result["learning_result"] = "recorded"
        elif action == "practice":
            items = practice_items(phase, state)
            answers = payload.get("answers", {})
            reveal = payload.get("reveal", False)
            if (type(reveal) is not bool or not isinstance(answers, dict)
                    or (not reveal and set(answers) != {item["id"] for _, item in items})):
                raise DeliveryError("Practice needs all displayed answer IDs, or reveal: true")
            prior = progress.setdefault("practice", [])
            exposed = any(attempt["revealed"] for attempt in prior)
            results = []
            for number, item in items:
                answer = "" if reveal else require_text(answers[item["id"]])
                evaluated = workbench(number).evaluate_question(item, answer, revealed=reveal)
                evaluated["independent"] = evaluated["correct"] and not exposed
                results.append(evaluated)
            prior.append(dict(at=now(), answers=answers, revealed=reveal, results=results))
            result.update(learning_result="revealed" if reveal else "practice", results=results)
        elif action in ("continue", "skip"):
            if action == "skip":
                progress["skip_reason"] = require_text(payload.get("reason"), "reason")
                progress["status"] = "skipped"
            else:
                kind = phase["kind"]
                if kind in ("prediction", "reflection", "checkpoint") and not progress["submissions"]:
                    raise DeliveryError("Record your explanation before continuing, or explicitly skip", 3)
                if phase["checkpoints"] and not all(progress["checks"].get(check, {}).get("correct") for check in phase["checkpoints"]):
                    raise DeliveryError("Revise the factual answers, or explicitly skip", 3)
                if kind == "feedback" and "feedback" not in progress:
                    raise DeliveryError("Submit feedback (an empty payload opts out), or skip", 3)
                progress["status"] = "pending_review" if kind == "review" else "complete"
                if any(not value["independent"] for value in progress["checks"].values()):
                    progress["status"] = "demonstrated"
                if "minutes" in payload:
                    if type(payload["minutes"]) not in (int, float) or not 0 <= payload["minutes"] <= 1440:
                        raise DeliveryError("Self-reported minutes must be between 0 and 1440")
                    progress["self_reported_minutes"] = payload["minutes"]
            if state["current"] == name:
                state["current"] = state["order"][position + 1] if position + 1 < len(state["order"]) else None
            result["learning_result"] = progress["status"]
        state["revision"] += 1
        state["updated_at"] = now()
        response = status_result(state, data, result)
        state["requests"][request["request_id"]] = dict(request=request, response=response)
        save_state(directory, state)
        return response


def export_session(ident: str) -> dict:
    data = definition()
    state = load_state(session_dir(ident), data)
    return dict(protocol_version=1, status="ok", session_id=ident, versions=state["versions"],
                completion=completion(state, data),
                phases=[dict(id=name, status=p["status"], checks=p["checks"], hints=p["hints"],
                             revealed=p["exposed"], attempts=len(p["submissions"])) for name, p in state["phases"].items()])


class JsonParser(argparse.ArgumentParser):
    def error(self, message):
        raise DeliveryError(message)


def learn(ident: str, mode: str = "solo", case: str = "A", pair_label: str | None = None) -> int:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise DeliveryError("learn needs a terminal; use session commands with --json for automation")
    if not session_dir(ident).exists():
        create_session(ident, mode, case, pair_label)
    print(f"\nNetwork Bootcamp · answers are saved under {session_dir(ident)}")
    print(f"Copyable commands assume: cd {shlex.quote(str(ROOT))}")
    print("Edit the three Markdown deliverables and ledger in your editor as you go.")
    print("Hints are free. Suggested times do not force a reveal. q saves your place and exits.")
    target = last_phase = None
    try:
        while True:
            view = session_status(ident, target)
            phase = view["phase"]
            if phase is None:
                print("\nYou reached the end of the delivery path. Review status:")
                for name, passed in view["completion"].items():
                    print(f"  {name.replace('_', ' ')}: {passed}")
                action = input("g: revisit a phase for revision/review · q: quit [q]: ").strip().lower() or "q"
            else:
                if phase["id"] != last_phase:
                    print(f"\n{phase['block_title']} · {phase['minutes']} suggested minutes\n")
                    print(phase["prompt"])
                    print(f"\n{phase['mode_prompt']}")
                    print("Artifacts: " + ", ".join(str(session_dir(ident) / name) for name in phase["artifacts"]))
                    if phase["break_after_minutes"]:
                        print(f"Take a {phase['break_after_minutes']}-minute break after this phase.")
                    last_phase = phase["id"]
                answered = phase["progress"]["submissions"] and all(check["correct"] for check in phase["progress"]["checks"].values())
                default = "r" if phase["kind"] == "review" and not phase["progress"]["reviews"] else "f" if phase["kind"] == "feedback" and "feedback" not in phase["progress"] else "c" if answered or phase["kind"] in ("review", "feedback") else "a"
                keys = {"a": "answer", "c": "continue", "s": "skip", "e": "evidence", "h": "hint", "v": "reveal", "r": "review", "f": "feedback", "p": "practice"}
                choices = [f"{key}: {value}" for key, value in keys.items() if value in phase["allowed_actions"]]
                action = input("\n" + " · ".join(choices) + f" · g: revisit · q: quit [{default}]: ").strip().lower() or default
            if action == "q":
                print(f"Saved. Resume with ./course learn --id {ident}")
                return 0
            if action == "g":
                print("\n".join(f"{p['id']}: {p['status']}" for p in view["released_phases"]))
                target = input("Phase ID (Enter returns to your current phase): ").strip() or None
                if target and target not in {p["id"] for p in view["released_phases"]}:
                    print("Choose a released phase ID.")
                    target = None
                last_phase = None
                continue
            if phase is None or action not in keys or keys[action] not in phase["allowed_actions"]:
                print("Choose an available action.")
                continue
            operation, payload = keys[action], {}
            try:
                if operation in ("answer", "predict"):
                    answers = {item["id"]: input(item["prompt"] + "\nAnswer: ") for item in phase["checkpoints"]}
                    payload = dict(text=input("Your prediction/explanation (one paragraph; artifacts can be edited separately): "), answers=answers)
                elif operation == "evidence":
                    for i, item in enumerate(phase["evidence"], 1):
                        print(f"{i}. {item['id']}: {item['command']}")
                    selected = int(input("Evidence view [1]: ").strip() or "1")
                    if not 1 <= selected <= len(phase["evidence"]):
                        raise DeliveryError("Choose a listed evidence number")
                    payload = {"view": phase["evidence"][selected - 1]["id"]}
                elif operation == "skip":
                    payload = {"reason": input("What remains unfinished, and why are you skipping it? ")}
                elif operation == "review":
                    print("Score mechanism, evidence, uncertainty, and action: 0 missing, 1 partial, 2 demonstrated.")
                    reviewer = input("Reviewer: self or facilitator [self]: ").strip() or "self"
                    scores = {name: int(input(f"{name} (0–2): ")) for name in DIMENSIONS}
                    payload = dict(reviewer=reviewer, scores=scores, feedback=input("Feedback and next revision: "))
                elif operation == "feedback":
                    for key, prompt in (("wanted_to_know", "I wanted to find out what happened next"), ("manageable", "The challenge felt manageable")):
                        value = input(f"{prompt} (1–5, Enter to omit): ").strip()
                        payload[key] = int(value) if value else None
                    text = input("What dragged, or needed more explanation? (optional): ").strip()
                    if text:
                        payload["text"] = text
                elif operation == "practice":
                    payload = {"answers": {item["id"]: input(item["prompt"] + "\nAnswer: ") for item in phase["practice"]}}
                elif operation == "continue":
                    value = input("Self-reported minutes for this phase (optional): ").strip()
                    if value:
                        payload["minutes"] = float(value)
                request = dict(request_id=uuid.uuid4().hex, expected_revision=view["revision"], phase_id=phase["id"], action=operation, payload=payload)
                response = act(ident, request)
                result = response["result"]
                if "output" in result:
                    print(result["output"]["stdout"])
                    if result["output"].get("stderr"):
                        print(result["output"]["stderr"], file=sys.stderr)
                if "text" in result:
                    print(result["text"])
                for name, check in result.get("checks", {}).items():
                    print(f"{name}: {check['feedback']}")
                for check in result.get("results", []):
                    print(f"{check['id']}: {check['learning_result']} · {check['feedback']}")
                if result.get("learning_result"):
                    print(result["learning_result"].replace("_", " "))
                if operation in ("continue", "skip"):
                    target = None
            except (DeliveryError, OSError, ValueError) as error:
                print(f"Could not record that action: {error}")
    except (EOFError, KeyboardInterrupt):
        print(f"\nAccepted responses are saved. Resume with ./course learn --id {ident}")
        return 0


def cli(argv: list[str]) -> int:
    """New commands have a strict JSON error path, including parser errors."""
    json_mode = "--json" in argv
    try:
        parser = JsonParser(prog="./course", description=__doc__)
        commands = parser.add_subparsers(dest="command", required=True)
        ready = commands.add_parser("doctor", help="read-only capability and evidence check")
        ready.add_argument("--json", action="store_true")
        terminal = commands.add_parser("learn", help="start or resume guided delivery")
        terminal.add_argument("--id", default="bootcamp")
        terminal.add_argument("--mode", choices=("solo", "pair"), default="solo")
        terminal.add_argument("--case", choices=("A", "B"), default="A")
        terminal.add_argument("--pair-label")
        session = commands.add_parser("session", help="saved course delivery")
        operations = session.add_subparsers(dest="operation", required=True)
        for name in ("create", "status", "act", "export"):
            operation = operations.add_parser(name)
            operation.add_argument("--id", required=True)
            operation.add_argument("--json", action="store_true")
            if name == "create":
                operation.add_argument("--mode", choices=("solo", "pair"), default="solo")
                operation.add_argument("--case", choices=("A", "B"), default="A")
                operation.add_argument("--pair-label")
                operation.add_argument("--seed", type=int, default=1)
            if name == "act":
                operation.add_argument("--input", required=True, help="JSON request file, or - for stdin")
            if name == "status":
                operation.add_argument("--phase", help="revisit a released phase without advancing")
            if name == "export":
                operation.add_argument("--format", choices=("json",), default="json")
        args = parser.parse_args(argv)
        if args.command == "learn":
            return learn(args.id, args.mode, args.case, args.pair_label)
        if args.command == "doctor":
            result = dict(protocol_version=1, status="ok", **doctor())
            code = 0 if result["ready"] else 4
        else:
            code = 0
            if args.operation == "create":
                result = create_session(args.id, args.mode, args.case, args.pair_label, args.seed)
            elif args.operation == "status":
                result = session_status(args.id, args.phase)
            elif args.operation == "export":
                result = export_session(args.id)
            else:
                with contextlib.nullcontext(sys.stdin) if args.input == "-" else open(args.input, encoding="utf-8") as handle:
                    raw = handle.read(131073)
                if len(raw) > 131072:
                    raise DeliveryError("Request exceeds 128 KiB")
                result = act(args.id, decode_json(raw))
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
        return code
    except (DeliveryError, OSError, ValueError, KeyError, TypeError) as error:
        code = error.code if isinstance(error, DeliveryError) else 4
        if json_mode:
            print(json.dumps(dict(protocol_version=1, status="error", error=str(error), code=code)))
        else:
            print(f"error: {error}", file=sys.stderr)
        return code
