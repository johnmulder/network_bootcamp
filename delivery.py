"""Local, deterministic delivery of the six-hour Network Bootcamp."""

from __future__ import annotations

import json
import re
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
