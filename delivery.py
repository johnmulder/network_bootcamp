"""Local, deterministic delivery of the six-hour Network Bootcamp."""

from __future__ import annotations

import argparse
import contextlib
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
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
                read_fragment(reference)
            if any(view not in EVIDENCE for view in phase["evidence"]):
                raise DeliveryError(f"Unknown evidence view: {name}")
            if any(check not in CHECKPOINTS for check in phase["checkpoints"]):
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
CHECKPOINTS = {"transfer.payload"}

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
    return list(EVIDENCE[view])


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
                 pair_label=pair_label, case=case, seed=seed, question_ids={},
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
                                 answer="1160 bytes", answers={"1160 bytes", "1160 byte", "1160 b"}),
    }
    return [items[name] for name in phase["checkpoints"]]


def public_checkpoint(item: dict) -> dict:
    return {key: item[key] for key in ("id", "prompt", "evidence")}


def render_references(references: list[dict], state: dict) -> str:
    return "\n\n".join(read_fragment(reference) for reference in references).replace(
        "work/bootcamp", f"work/{state['id']}")


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


def status_result(state: dict, data: dict, result: dict | None = None) -> dict:
    current = state["current"]
    view = None
    if current:
        phase = phase_by_id(data, current)
        view = {key: phase[key] for key in ("id", "block", "kind", "minutes", "artifacts")}
        view.update(prompt=render_references(phase["content"], state),
                    checkpoints=[public_checkpoint(item) for item in checkpoint_items(phase, state)],
                    evidence=[dict(id=name, command=shlex.join(evidence_command(name, state))) for name in phase["evidence"]],
                    allowed_actions=allowed_actions(phase),
                    progress=copy.deepcopy(state["phases"][current]))
    return dict(protocol_version=1, status="ok", session_id=state["id"], revision=state["revision"],
                phase=view, completion=completion(state, data), result=result,
                workspace=f"work/{state['id']}")


def session_status(ident: str) -> dict:
    data = definition()
    return status_result(load_state(session_dir(ident), data), data)


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
                correct = " ".join(answer.lower().split()) in item["answers"]
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


def cli(argv: list[str]) -> int:
    """New commands have a strict JSON error path, including parser errors."""
    json_mode = "--json" in argv
    try:
        parser = JsonParser(prog="./course", description=__doc__)
        commands = parser.add_subparsers(dest="command", required=True)
        ready = commands.add_parser("doctor", help="read-only capability and evidence check")
        ready.add_argument("--json", action="store_true")
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
            if name == "export":
                operation.add_argument("--format", choices=("json",), default="json")
        args = parser.parse_args(argv)
        if args.command == "doctor":
            result = dict(protocol_version=1, status="ok", **doctor())
            code = 0 if result["ready"] else 4
        else:
            code = 0
            if args.operation == "create":
                result = create_session(args.id, args.mode, args.case, args.pair_label, args.seed)
            elif args.operation == "status":
                result = session_status(args.id)
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
