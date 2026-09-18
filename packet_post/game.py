"""Durable practice actions. This module never imports tcod or opens a window."""

from __future__ import annotations

import copy
import fcntl
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from . import content

SCHEMA = 1
LIMIT = 2 * 1024 * 1024
STAGES = {"brief", "decision", "feedback", "debrief", "complete"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fresh():
    return dict(schema=SCHEMA, content_sha256=content.fingerprint(), current=None,
                progress={}, stamps=[], seed=1, settings=dict(plain=False, contrast=False, scale=2))


class Game:
    def __init__(self, state=None):
        self.reviewed = set()
        self.state = fresh() if state is None else state
        self.validate()

    def authorize(self, session_id):
        """Read existing reviews only; never mutate or award course attainment."""
        try:
            status = content.delivery.session_status(session_id)
        except (content.delivery.DeliveryError, OSError, ValueError) as error:
            raise ValueError(f"Cannot read course reviews: {error}") from None
        self.reviewed = {phase for phase, reviews in status["reviews"].items()
                         if any(r.get("valid_pass") is True for r in reviews.values())}

    def available(self, ident):
        return set(content.mission(ident).get("requires", [])) <= self.reviewed

    def validate(self):
        s = self.state
        if not isinstance(s, dict) or set(s) != set(fresh()):
            raise ValueError("Unrecognized game save. Keep it and restore a matching game copy.")
        if s["schema"] != SCHEMA or s["content_sha256"] != content.fingerprint():
            raise ValueError("Save belongs to a different game/content version. Use its matching copy or a new --id.")
        ids = {m["id"] for m in content.missions()}
        if s["current"] is not None and s["current"] not in s["progress"]:
            raise ValueError("Invalid current mission.")
        if not isinstance(s["progress"], dict) or not set(s["progress"]) <= ids:
            raise ValueError("Invalid mission history.")
        for ident, p in s["progress"].items():
            if not isinstance(p, dict) or set(p) != {"index", "stage", "attempts", "help", "opened", "reflection", "draft"}:
                raise ValueError("Invalid mission save.")
            steps = content.mission(ident)["steps"]
            if type(p["index"]) is not int or not 0 <= p["index"] < len(steps) or p["stage"] not in STAGES:
                raise ValueError("Invalid mission position.")
            for key in ("attempts", "help", "opened"):
                if not isinstance(p[key], dict) or not set(p[key]) <= set(steps):
                    raise ValueError("Invalid practice history.")
            for step, attempts in p["attempts"].items():
                if not isinstance(attempts, list) or any(not isinstance(a, dict) or
                        set(a) != {"at", "values", "reason", "supported", "result"} for a in attempts):
                    raise ValueError("Invalid attempt history.")
                for a in attempts:
                    if not isinstance(a["reason"], str) or type(a["supported"]) is not bool:
                        raise ValueError("Invalid attempt fields.")
                    if a["result"] != content.evaluate(content.scenes()[step], a["values"]):
                        raise ValueError("Saved result disagrees with its recorded choice.")
            for step, opened in p["opened"].items():
                allowed = {c["id"] for c in content.scenes()[step].cards}
                if not isinstance(opened, list) or any(c not in allowed for c in opened):
                    raise ValueError("Invalid evidence history.")
            if any(type(v) is not bool for v in p["help"].values()) or not isinstance(p["reflection"], dict):
                raise ValueError("Invalid support or reflection history.")
            draft = p["draft"]
            if not isinstance(draft, dict) or set(draft) != {"values", "reason"} or not isinstance(draft["values"], dict) or not isinstance(draft["reason"], str):
                raise ValueError("Invalid unfinished notes.")
            if len(json.dumps(draft)) > 16000:
                raise ValueError("Unfinished notes are too large.")
            field_specs = ({name: {} for name in ("mechanism", "evidence", "uncertainty", "action")}
                           if p["stage"] in {"debrief", "complete"} else
                           {f["key"]: f for f in content.scenes()[steps[p["index"]]].fields})
            if not set(draft["values"]) <= set(field_specs):
                raise ValueError("Draft belongs to an unexpected decision.")
            for key, value in draft["values"].items():
                spec = field_specs[key]
                if spec.get("multiple"):
                    if not isinstance(value, list) or any(not isinstance(v, str) or v not in spec["options"] for v in value):
                        raise ValueError("Invalid draft selection.")
                elif not isinstance(value, str) or len(value) > 1600:
                    raise ValueError("Invalid draft text.")
            if p["stage"] == "feedback" and not p["attempts"].get(steps[p["index"]]):
                raise ValueError("Feedback has no committed attempt.")
            completed = steps if p["stage"] in {"debrief", "complete"} else steps[:p["index"]]
            if any(not p["attempts"].get(step) or not p["attempts"][step][-1]["result"]["correct"] for step in completed):
                raise ValueError("Mission position skips an unfinished decision.")
            if any(not isinstance(v, str) or not v.strip() or len(v) > 1600 for v in p["reflection"].values()):
                raise ValueError("Invalid reflection text.")
            if p["stage"] == "complete" and set(p["reflection"]) != {"mechanism", "evidence", "uncertainty", "action"}:
                raise ValueError("Completed practice is missing its reflection.")
        settings = s["settings"]
        if not isinstance(settings, dict) or set(settings) != {"plain", "contrast", "scale"} or any(
                type(settings[k]) is not bool for k in ("plain", "contrast")) or type(settings["scale"]) is not int or not 1 <= settings["scale"] <= 3:
            raise ValueError("Invalid display settings.")
        if s["seed"] != 1 or not isinstance(s["stamps"], list) or any(not isinstance(v, str) for v in s["stamps"]):
            raise ValueError("Invalid game metadata.")
        earned = {content.mission(ident)["stamp"] for ident, p in s["progress"].items() if p["stage"] == "complete"}
        if len(s["stamps"]) != len(set(s["stamps"])) or set(s["stamps"]) != earned:
            raise ValueError("Stamps do not match completed practice.")

    @property
    def progress(self):
        return self.state["progress"][self.state["current"]]

    @property
    def scene(self):
        return content.scenes()[content.mission(self.state["current"])["steps"][self.progress["index"]]]

    def start(self, ident):
        mission = content.mission(ident)
        if not self.available(ident):
            raise ValueError("This post-lesson mission needs current passing reviews for " +
                             ", ".join(mission["requires"]) + ". Launch with --course-session YOUR-ID after those reviews.")
        self.state["current"] = ident
        self.state["progress"].setdefault(ident, dict(index=0, stage="brief", attempts={}, help={}, opened={}, reflection={}, draft=dict(values={}, reason="")))

    def draft(self, values, reason):
        self.progress["draft"] = dict(values=copy.deepcopy(values), reason=reason)

    def begin(self):
        if self.progress["stage"] != "brief":
            raise ValueError("This mission has already begun.")
        self.progress["stage"] = "decision"

    def visible(self):
        if self.state["current"] is None or not self.available(self.state["current"]):
            return None
        p, scene = self.progress, self.scene
        view = dict(mission=content.mission(self.state["current"]), stage=p["stage"],
                    index=p["index"], scene=scene.public(), opened=p["opened"].get(scene.id, []),
                    attempts=len(p["attempts"].get(scene.id, [])), supported=p["help"].get(scene.id, False),
                    reflection=p["reflection"])
        if p["stage"] == "feedback":
            view["last"] = p["attempts"][scene.id][-1]
        return copy.deepcopy(view)

    def inspect(self, ident):
        if not self.available(self.state["current"]):
            raise ValueError("These post-lesson records are not released for this game launch.")
        if self.progress["stage"] not in {"decision", "feedback"}:
            raise ValueError("Open evidence during a decision.")
        item = next((c for c in self.scene.cards if c["id"] == ident), None)
        if item is None:
            raise ValueError("That evidence is not released in this scene.")
        opened = self.progress["opened"].setdefault(self.scene.id, [])
        if ident not in opened:
            opened.append(ident)
        return content.evidence(item)

    def hint(self):
        if self.progress["stage"] != "decision":
            raise ValueError("Hints belong to an active prediction.")
        self.progress["help"][self.scene.id] = True
        return self.scene.hint

    def commit(self, values, reason):
        if self.progress["stage"] != "decision":
            raise ValueError("This prediction is already committed. Continue or choose Retry.")
        if not isinstance(reason, str) or not reason.strip() or len(reason) > 1600:
            raise ValueError("Add a short reason before committing (up to 1600 characters).")
        result = content.evaluate(self.scene, values)
        attempts = self.progress["attempts"].setdefault(self.scene.id, [])
        attempts.append(dict(at=now(), values=copy.deepcopy(values), reason=reason.strip(),
                             supported=bool(attempts) or self.progress["help"].get(self.scene.id, False), result=result))
        self.progress["stage"] = "feedback"
        self.draft({}, "")

    def retry(self):
        if self.progress["stage"] != "feedback":
            raise ValueError("Commit a prediction before retrying.")
        self.progress["help"][self.scene.id] = True
        self.progress["stage"] = "decision"
        self.draft({}, "")

    def advance(self):
        if self.progress["stage"] != "feedback" or not self.progress["attempts"][self.scene.id][-1]["result"]["correct"]:
            raise ValueError("Correct the factual decision, with help if useful, before continuing.")
        if self.progress["index"] + 1 == len(content.mission(self.state["current"])["steps"]):
            self.progress["stage"] = "debrief"
        else:
            self.progress["index"] += 1
            self.progress["stage"] = "decision"
        self.draft({}, "")

    def reflect(self, fields):
        if self.progress["stage"] != "debrief" or set(fields) != {"mechanism", "evidence", "uncertainty", "action"}:
            raise ValueError("Complete the four debrief fields.")
        if any(not isinstance(v, str) or not v.strip() or len(v) > 1600 for v in fields.values()):
            raise ValueError("Write a short response in each field.")
        if self.state["current"] == "handoff" and sum(len(v.split()) for v in fields.values()) > 150:
            raise ValueError("Keep the handoff within 150 words across the four fields.")
        self.progress["reflection"] = dict(fields)
        self.progress["stage"] = "complete"
        stamp = content.mission(self.state["current"])["stamp"]
        if stamp not in self.state["stamps"]:
            self.state["stamps"].append(stamp)

    def journal(self):
        lines = ["# Packet Post practice journal", "", "Practice only; no course attainment or prose grade is awarded.", ""]
        for ident, p in self.state["progress"].items():
            lines += ["## " + content.mission(ident)["title"], "", "Lesson: " + content.mission(ident)["lesson"], ""]
            for step, attempts in p["attempts"].items():
                lines += ["### " + content.scenes()[step].title, ""]
                for a in attempts:
                    label = "supported practice" if a["supported"] else "first unassisted practice attempt"
                    lines += [f"{a['at']} | {label} | factual match: {a['result']['correct']}",
                              "", "Prediction: " + json.dumps(a["values"]), "", "Reason: " + a["reason"],
                              "", "Feedback: " + a["result"]["explanation"], "",
                              "Unknowns: " + "; ".join(a["result"]["unknowns"]), ""]
                    if "model" in a["result"]:
                        lines += ["Bounded model result:", "", "```json", json.dumps(a["result"]["model"], indent=2), "```", ""]
                lines += ["Available sources: " + ", ".join(content.source_name(c) for c in content.scenes()[step].cards),
                          "", "Opened cards: " + ", ".join(p["opened"].get(step, [])), ""]
            for name, value in p["reflection"].items():
                lines += [f"{name.title()}: {value}", ""]
        return "\n".join(lines)


class Save:
    """One local writer; failed validation or writes never replace the previous save."""

    def __init__(self, ident="night-shift", root=None):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,39}", ident):
            raise ValueError("Use a save ID of 1-40 lowercase letters, digits or hyphens.")
        base = Path(root) if root is not None else content.ROOT / "work/packet-post"
        for path in (base, base / ident, content.ROOT / "work" if root is None else base):
            if path.is_symlink():
                raise ValueError("Save directories must not be symbolic links.")
        # macOS /var and /tmp are system aliases; canonicalize the trusted root.
        self.path = base.resolve() / ident
        self.lock = None

    def __enter__(self):
        marker = self.path / ".packet-post"
        if self.path.exists() and (not marker.is_file() or marker.is_symlink() or marker.read_text() != "Packet Post 1\n"):
            raise ValueError("That directory is not a Packet Post save. Choose another --id.")
        self.path.mkdir(parents=True, exist_ok=True)
        if not marker.exists():
            with marker.open("x") as handle:
                handle.write("Packet Post 1\n")
        lockpath = self.path / ".lock"
        self.lock = os.fdopen(os.open(lockpath, os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600), "w")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock.close()
            raise ValueError("This save is open in another Packet Post process. Close it or choose another --id.") from None
        return self

    def __exit__(self, *args):
        if self.lock:
            self.lock.close()

    def load(self):
        path = self.path / "state.json"
        if not path.exists() and not path.is_symlink():
            return Game()
        if path.is_symlink() or not path.is_file() or path.stat().st_size > LIMIT:
            raise ValueError("Invalid or oversized save; preserve it and start with a new --id.")
        try:
            return Game(json.loads(path.read_text()))
        except (ValueError, TypeError, KeyError, IndexError, AttributeError) as error:
            raise ValueError(f"Cannot load save: {error}. Original kept; choose a new --id or restore a matching copy.") from None

    def write(self, game):
        game.validate()
        raw = json.dumps(game.state, indent=2) + "\n"
        if len(raw.encode()) > LIMIT:
            raise ValueError("Save reached its size limit. Export the journal and use a new --id.")
        path = self.path / "state.json"
        if path.is_symlink():
            raise ValueError("Save file must not be a symbolic link.")
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=self.path, prefix=".save-", delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if temporary and temporary.exists():
                temporary.unlink()

    def export(self, game):
        for number in range(1, 10000):
            path = self.path / f"journal-{number:04}.md"
            try:
                with path.open("x") as handle:
                    handle.write(game.journal())
                return path
            except FileExistsError:
                continue
        raise ValueError("Journal directory is full; keep existing exports and use another save ID.")
