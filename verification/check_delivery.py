#!/usr/bin/env python3
"""Check content contracts and optionally rehearse delivery with real tools."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import delivery as d


def markdown_files():
    return sorted(path for path in ROOT.rglob("*.md")
                  if not any(part in {"work", ".git", "__pycache__"} for part in path.relative_to(ROOT).parts))


def anchors(text):
    result, counts, fence = set(), {}, None
    for line in text.splitlines():
        marker = re.match(r"\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
            continue
        if fence or not re.match(r"^#{1,6} ", line):
            continue
        heading = re.sub(r"^#+ ", "", line).strip().lower()
        heading = re.sub(r"[^\w -]", "", heading).replace(" ", "-")
        count = counts.get(heading, 0)
        counts[heading] = count + 1
        result.add(heading + (f"-{count}" if count else ""))
    return result


def content_checks():
    data = d.definition()
    d.evidence_integrity()
    errors, count = [], 0
    if not data["learning_contract"]["enabled"]:
        errors.append("Learning contract is unfinished or inactive")
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            if re.match(r"[a-zA-Z][\w+.-]*:", target):
                continue
            relative, _, anchor = unquote(target).partition("#")
            destination = (path.parent / relative).resolve() if relative else path
            count += 1
            if not destination.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing link {target}")
            elif anchor and destination.suffix == ".md" and anchor not in anchors(destination.read_text(encoding="utf-8")):
                errors.append(f"{path.relative_to(ROOT)}: missing anchor {target}")
    used = set()
    for case in ("A", "B"):
        state = dict(case=case, id="verification")
        for phase in data["phases"]:
            if not phase["implemented"]:
                errors.append(f"Unfinished phase: {phase['id']}")
            prompt = d.render_references(phase["content"], state)
            permitted = [d.evidence_command(view, state) for view in phase["evidence"]]
            used.update(phase["evidence"])
            for fence in re.findall(r"```sh\n(.*?)```", prompt, re.S):
                for command in fence.splitlines():
                    if command.strip() and not command.startswith("#") and shlex.split(command) not in permitted:
                        errors.append(f"{phase['id']}: command differs from its registered evidence view: {command}")
    if used != set(d.EVIDENCE):
        errors.append(f"Unused or missing evidence IDs: {used ^ set(d.EVIDENCE)}")
    for view, command in d.EVIDENCE.items():
        if command[0] == "tshark" and ("-n" not in command or "-r" not in command):
            errors.append(f"{view}: TShark must disable name resolution and read a saved file")
        for argument in command:
            if argument.startswith("labs/fixtures/") and not d.confined(ROOT, argument).is_file():
                errors.append(f"{view}: missing evidence file {argument}")
    if errors:
        raise d.DeliveryError("\n".join(errors), 4)
    print(f"Content checks passed: {len(data['phases'])} phases, {len(used)} evidence views, {count} local links.", flush=True)


def smoke():
    readiness = d.doctor()
    if not readiness["ready"]:
        raise d.DeliveryError(json.dumps(readiness), 4)
    for view in d.EVIDENCE:
        result = d.run_tool(d.evidence_command(view, {"case": "A"}))
        if result["returncode"] != 0 or result["truncated"] or not result["stdout"].strip():
            raise d.DeliveryError(f"Evidence smoke failed: {view}", 4, result)
    print(f"Real-tool smoke passed: {len(d.EVIDENCE)} read-only evidence views.", flush=True)


def journey(case):
    """Use fresh CLI processes and explicit synthetic answers, never TTY input."""
    examples = d.module_at("tests/test_delivery.py")
    ident = "verify-" + uuid.uuid4().hex
    directory = d.session_dir(ident)
    created = False
    before = d.versions(d.definition())

    def call(*arguments, request=None, json_output=True):
        result = subprocess.run([str(ROOT / "course"), *arguments], cwd=ROOT.parent,
                                input=json.dumps(request) if request is not None else "",
                                text=True, capture_output=True, timeout=60)
        if result.returncode:
            raise d.DeliveryError(f"CLI rehearsal failed: {result.stdout}\n{result.stderr}", 4)
        return json.loads(result.stdout) if json_output else result.stdout

    try:
        view = call("session", "create", "--id", ident, "--case", case, "--mode", "solo" if case == "A" else "pair", "--json")
        created = True

        def act(action, payload=None, phase_id=None):
            nonlocal view
            request = dict(request_id=uuid.uuid4().hex, expected_revision=view["revision"],
                           phase_id=phase_id or view["phase"]["id"], action=action, payload=payload or {})
            view = call("session", "act", "--id", ident, "--input", "-", "--json", request=request)
            return request

        while view["phase"]:
            phase = view["phase"]
            if phase.get("initial_diagnosis_required"):
                assert not phase["checkpoints"] and not phase["evidence"] and not phase["assessment"] and not phase["artifact_regions"]
                act("diagnose", examples.DIAGNOSIS)
                phase = view["phase"]
            if phase["id"] == "c01.model":
                act("skip", {"reason": "Rehearsal of revisiting unfinished work"})
                act("answer", {"text": "A synthetic learner revisits the first-hop prediction."}, phase_id=phase["id"])
                act("continue", phase_id=phase["id"])
                continue
            for evidence in phase["evidence"]:
                act("evidence", {"view": evidence["id"]})
            if phase["kind"] in ("prediction", "reflection", "checkpoint"):
                answers = examples.answers_for(phase, case)
                if phase["id"] == "c02.calculate":
                    act("answer", {"text": "First synthetic attempt.", "answers": {"transfer.payload": "1200 bytes"}})
                    assert view["result"]["learning_result"] == "incorrect"
                    view = call("session", "status", "--id", ident, "--json")
                    act("hint")
                request = act("answer", {"text": "PRIVATE REHEARSAL TEXT: fixture-backed mechanics, not a learner assessment.", "answers": answers})
                assert view["result"]["learning_result"] != "incorrect"
                if phase["id"] == "opening.predict":
                    assert call("session", "act", "--id", ident, "--input", "-", "--json", request=request) == view
                if phase["id"] == "c02.calculate":
                    act("reassess", {"family": "transfer"})
                    problem = view["result"]["problem_result"]
                    payload = "1224 bytes" if problem["id"] == "transfer-r1" else "1440 bytes"
                    act("problem_answer", {"variant_id": problem["id"], "answers": {"payload": payload, "fits": "yes"}})
                    assert view["result"]["problem_result"]["independent"]
            elif phase["kind"] == "feedback":
                act("feedback", {"wanted_to_know": 4, "manageable": 4})
            elif phase["id"] == "c02.review":
                act("reveal")
            if phase["id"] in examples.EXPERIMENTS:
                act("experiment_predict", dict(parameters=examples.EXPERIMENTS[phase["id"]], prediction="PRIVATE prediction: bounded effect with unknown recovery."))
                assert "result" not in view["result"]["experiment"]
                experiment_id = view["result"]["experiment"]["id"]
                act("experiment_result", {"experiment_id": experiment_id})
                assert view["result"]["experiment"]["result"]["unknowns"]
            if phase["id"] == "opening.reflect":
                for example, scores in (("calibration-symptom", dict.fromkeys(d.DIMENSIONS, 0)), ("calibration-partial", dict(mechanism=2, evidence=2, uncertainty=0, action=1))):
                    act("calibrate", dict(example_id=example, scores=scores))
            act("continue")
        assert view["completion"]["delivery_finished"]
        assert not view["completion"]["self_reviewed_completion"]
        examples.fill_rehearsal_artifacts(directory, case)
        current = call("session", "status", "--id", ident, "--phase", "c05.narrative", "--json")
        region = current["phase"]["artifact_regions"][0]
        artifact_before = (directory / region["file"]).read_bytes()
        act("submit_artifact", dict(file=region["file"], region=region["region"], expected_sha256=region["sha256"], answers={}, confidence="medium"), phase_id="c05.narrative")
        act("continue", phase_id="c05.narrative")
        assert (directory / region["file"]).read_bytes() == artifact_before
        for name in [p["id"] for p in d.definition()["phases"] if p["kind"] == "review"]:
            review = call("session", "status", "--id", ident, "--phase", name, "--json")
            act("review", dict(reviewer="self", scores=dict.fromkeys(d.DIMENSIONS, 2),
                               reasoning=examples.REASONING,
                               feedback="Synthetic review exercises the recording contract only.",
                               expected_artifact_hashes=review["phase"]["artifact_hashes"],
                               expected_response_sha256=review["phase"]["response_sha256"]), phase_id=name)
        summary = call("session", "export", "--id", ident, "--format", "json")
        assert summary["completion"]["self_reviewed_completion"]
        assert not summary["completion"]["facilitator_reviewed_completion"]
        assert "PRIVATE REHEARSAL TEXT" not in json.dumps(summary)
        rows = call("session", "export", "--id", ident, "--format", "csv", json_output=False)
        assert len(list(csv.DictReader(io.StringIO(rows)))) == len(d.definition()["phases"])
        objectives = call("session", "export", "--id", ident, "--format", "objectives-csv", json_output=False)
        objectives = list(csv.DictReader(io.StringIO(objectives)))
        assert len(objectives) == 25
        transfer = next(o for o in objectives if o["family"] == "transfer")
        assert transfer["first_response_correct"] == "False" and transfer["supported_correct"] == "True" and transfer["fresh_independent"] == "True"
        assert "PRIVATE REHEARSAL TEXT" not in json.dumps(objectives)
        call("session", "export", "--id", ident, "--format", "json", "--include-artifacts", "--output", "review.json")
        with tempfile.TemporaryDirectory(prefix="moved-review-") as temp:
            moved = Path(temp) / "review.json"
            shutil.copyfile(directory / "exports/review.json", moved)
            bundle = json.loads(moved.read_text())
            assert set(bundle["included_files"]) == set(d.ARTIFACTS)
            assert bundle["versions"] == before
        d.evidence_integrity()
        assert before == d.versions(d.definition())
        print(f"Fresh-process journey passed: main {case}, exit {'B' if case == 'A' else 'A'}, {len(d.definition()['phases'])} phases, resume/retry, review and export. Synthetic results only.", flush=True)
    finally:
        if created:
            shutil.rmtree(directory)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true", help="execute every real read-only evidence view")
    parser.add_argument("--journey", action="store_true", help="rehearse both assignments using fresh JSON CLI processes")
    args = parser.parse_args()
    try:
        content_checks()
        if args.smoke:
            smoke()
        if args.journey:
            for case in ("A", "B"):
                journey(case)
        return 0
    except (d.DeliveryError, OSError, ValueError, AssertionError, subprocess.SubprocessError) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
