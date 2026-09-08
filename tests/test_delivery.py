"""Contracts and journeys for local course delivery."""

import copy
import contextlib
import csv
import io
import json
import shlex
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import delivery as d

ANSWERS = {
    "opening.local": "yes", "opening.dns": "no", "opening.application": "no",
    "m1.routes.10.0.20.40": "10.0.20.40/32",
    "m1.convergence.remove-host-route": "10.0.20.0/24",
    "route.before-hops": "10.0.10.252", "route.after-hops": "10.0.10.253, 10.0.10.254",
    "transfer.payload": "1160 bytes", "m1.convergence.interval": "80 ms",
    "m1.convergence.next-hop": "10.255.0.3", "m1.convergence.application": "no",
    "routing.bgp-peer": "192.0.2.2", "routing.corp-route": "0.0.0.0/0",
    "routing.ot-route": "no route", "m2.cloud.corp-vpc.10.0.20.40": "on-prem",
    "m2.cloud.on-prem.10.20.5.10": "corp-vpc", "flows.server-ot": "allow",
    "flows.user-ot": "deny", "budget.options": "state-sync, monitoring",
    "incident.utc": "2026-08-15T16:04:01Z", "incident.auth-record": "2",
}
DIAGNOSIS = dict(hypotheses=["Forwarding or state may have changed.", "The service may not be responding."],
                 confidence="low", next_evidence="observations")
EXPERIMENTS = {
    "c01.change": dict(condition="remove-host-route", destination="10.0.20.40"),
    "c02.calculate": dict(scenario="plain", payload=1161),
    "c04.outcomes": dict(options=["state-sync", "monitoring"], failure="session-sync-stale", twist=False),
    "c04.twist": dict(options=["backup-path", "management"], failure="power-loss", twist=True),
}
REASONING = dict(claim="Assessed region: mechanism field", evidence="Assessed region: cited source and record",
                 limitation="Assessed region: unresolved alternative", next_test="Assessed region: owner and validation")


def answers_for(phase, main_case):
    letter = ("B" if main_case == "A" else "A") if phase["block"] == "exit" else main_case
    answers = {**ANSWERS, "case.id": f"{letter}-v1", "case.change": "10.20.0.0/16" if letter == "A" else "ISOLATED",
               "case.lookup": "no route", "case.observation": "A3" if letter == "A" else "B2"}
    return {item["id"]: answers[item["id"]] for item in phase["checkpoints"]}


def fill_rehearsal_artifacts(directory, case="A"):
    """Synthetic structural fixtures, never examples of graded learner prose."""
    references = [("flows", 1), ("endpoint", 1), ("endpoint", 2), ("auth", 2), ("firewall", 1), ("siem", 1)]
    for name in ("packet-path.md", "architecture.md", "incident.md"):
        path = directory / name
        text = (d.ROOT / d.ARTIFACTS[name]).read_text()
        if name == "incident.md":
            text = text.replace("Evidence IDs: ___", "Evidence IDs: " + ", ".join(f"incident/{source}.jsonl#{number}" for source, number in references), 1)
            text = text.replace("Evidence IDs: ___", "Evidence IDs: " + ("A3" if case == "A" else "B2"), 1)
        text = text.replace("___", f"{case}-v1 PRIVATE REHEARSAL TEXT")
        text = re.sub(r"(?<=\|)[ \t]*(?=\|)", " Unknown; rehearsal entry ", text)
        path.write_text(text)
    with (directory / "evidence-ledger.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=d.workbench(3).LEDGER_FIELDS)
        writer.writeheader()
        rows = []
        for source, number in references:
            filename = f"incident/{source}.jsonl"
            record = d.workbench(3).read_jsonl(filename)[number - 1]
            rows.append((filename, f"{filename}#{number}", record.get("time", record.get("start"))))
        data = d.workbench(1).read_json(f"challenges/case-{case.lower()}.json")
        decisive = next(r for r in data["observations"] if r["id"] == ("A3" if case == "A" else "B2"))
        rows.append((f"challenges/case-{case.lower()}.json", decisive["id"], decisive["time"]))
        for source, evidence_id, raw in rows:
            writer.writerow(dict(evidence_id=evidence_id, source=source, collection_point="unknown",
                                 raw_time=raw, normalized_time=raw, entity="fixture entity",
                                 observation="Scripted observation, not a learner result", classification="observed",
                                 limitation="Reasoning quality requires human review", confidence="medium"))


class DefinitionTests(unittest.TestCase):
    def test_definition_and_schedule(self):
        data = d.definition()
        self.assertEqual(sum(block["minutes"] for block in data["blocks"]), 360)
        self.assertEqual(sum(block["break_after"] for block in data["blocks"]), 60)
        for mutate in (
            lambda value: value["phases"][1].update(id=value["phases"][0]["id"]),
            lambda value: value["phases"][0].update(prerequisites=["exit.feedback"]),
            lambda value: value["phases"][0].update(minutes=200),
            lambda value: next(p for p in value["phases"] if p["id"] == "c02.inspect").update(evidence=["shell"]),
            lambda value: next(p for p in value["phases"] if p["id"] == "c02.calculate").update(checkpoints=["missing"]),
            lambda value: value["phases"][3]["artifact_bindings"][0].update(region="missing"),
        ):
            changed = copy.deepcopy(data)
            mutate(changed)
            with self.assertRaises(d.DeliveryError):
                d.validate_definition(changed)

    def test_fragment_boundaries_and_bad_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "brief.md"
            path.write_text("<!-- delivery:start first -->\nQuestion\n<!-- delivery:end first -->\nSecret\n")
            self.assertEqual(d.fragments(path), {"first": "Question"})
            for text in (
                "<!-- delivery:start first -->\n<!-- delivery:start nested -->",
                "<!-- delivery:end missing -->",
                "<!-- delivery:start missing -->",
                "<!-- delivery:start a -->\n<!-- delivery:end a -->\n<!-- delivery:start a -->",
            ):
                path.write_text(text)
                with self.assertRaises(d.DeliveryError):
                    d.fragments(path)
            with self.assertRaises(d.DeliveryError):
                d.confined(Path(temp), "../escape")
        with self.assertRaises(d.DeliveryError):
            d.read_fragment({"path": "challenges/02-the-transfer-that-stops.md", "fragment": "missing"})


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = mock.patch.object(d, "WORK_ROOT", Path(self.temp.name))
        self.work.start()
        self.addCleanup(self.work.stop)
        self.ready = mock.patch.object(d, "doctor", return_value={"ready": True})
        self.ready.start()
        self.addCleanup(self.ready.stop)
        self.view = d.create_session("learner")

    def request(self, action, payload=None, phase=None):
        view = d.session_status("learner")
        return dict(request_id=f"request-{view['revision']}", expected_revision=view["revision"],
                    phase_id=phase or view["phase"]["id"], action=action, payload=payload or {})

    def act(self, action, payload=None, phase=None):
        self.view = d.act("learner", self.request(action, payload, phase))
        return self.view

    def experiment(self, phase):
        result = self.act("experiment_predict", dict(parameters=EXPERIMENTS[phase], prediction="PRIVATE prediction: explain the relevant bound or remaining dependency."))
        return self.act("experiment_result", {"experiment_id": result["result"]["experiment"]["id"]})

    def reach_transfer(self):
        while self.view["phase"]["id"] != "c02.predict":
            self.act("skip", {"reason": "Test setup for transfer slice"})

    def finish_day(self):
        while self.view["phase"]:
            phase = self.view["phase"]
            if phase.get("initial_diagnosis_required"):
                self.act("diagnose", DIAGNOSIS)
                phase = self.view["phase"]
            if phase["kind"] in ("prediction", "reflection", "checkpoint"):
                self.act("answer", {"text": "PRIVATE REHEARSAL TEXT: inspect the record and qualify the claim.", "answers": answers_for(phase, "A")})
            elif phase["kind"] == "feedback":
                self.act("feedback", {})
            if phase["id"] in EXPERIMENTS:
                self.experiment(phase["id"])
            self.act("continue")

    def review(self, phase, reviewer="self", score=2, hashes=None):
        view = d.session_status("learner", phase)
        return self.act("review", dict(reviewer=reviewer, scores=dict.fromkeys(d.DIMENSIONS, score),
                        reasoning=REASONING,
                        feedback="PRIVATE REHEARSAL TEXT: synthetic review", expected_artifact_hashes=hashes if hashes is not None else view["phase"]["artifact_hashes"],
                        expected_response_sha256=view["phase"]["response_sha256"]), phase)

    def test_transfer_prediction_correction_resume_and_retry(self):
        self.reach_transfer()
        before = (d.session_dir("learner") / "session.json").read_bytes()
        with self.assertRaises(d.DeliveryError):
            self.act("continue")
        self.assertEqual((d.session_dir("learner") / "session.json").read_bytes(), before)
        request = self.request("predict", {"text": "Size-dependent failure or endpoint handling."})
        first = d.act("learner", request)
        self.assertEqual(d.act("learner", request), first)
        with self.assertRaises(d.DeliveryError):
            d.act("learner", {**request, "payload": {"text": "Different"}})
        self.act("continue")
        with mock.patch.object(d, "run_tool", return_value=dict(returncode=0, truncated=False, stdout="frame observations")):
            self.act("evidence", {"view": "transfer.fields"})
        self.act("answer", {"text": "The sequence repeats after ICMP at this capture point."})
        self.act("continue")
        wrong = self.act("answer", {"text": "Subtract headers.", "answers": {"transfer.payload": "1160 bits"}})
        self.assertEqual(wrong["result"]["learning_result"], "incorrect")
        self.act("hint")
        self.act("answer", {"text": "Subtract both 20-byte headers.", "answers": {"transfer.payload": "1160 bytes"}})
        resumed = d.session_status("learner")
        self.assertEqual(len(resumed["phase"]["progress"]["submissions"]), 2)
        self.assertFalse(resumed["phase"]["progress"]["checks"]["transfer.payload"]["independent"])
        self.experiment("c02.calculate")
        self.act("continue")
        self.act("continue")
        exported = d.export_session("learner")
        self.assertNotIn("Subtract headers", json.dumps(exported))
        self.assertFalse(exported["completion"]["facilitator_reviewed_completion"])

    def test_create_and_failed_save_preserve_work(self):
        path = d.session_dir("learner") / "packet-path.md"
        path.write_text("My existing notes")
        with self.assertRaises(d.DeliveryError):
            d.create_session("learner")
        self.assertEqual(path.read_text(), "My existing notes")
        state_path = d.session_dir("learner") / "session.json"
        before = state_path.read_bytes()
        with mock.patch.object(d.os, "replace", side_effect=OSError("interrupted write")):
            with self.assertRaises(OSError):
                self.act("skip", {"reason": "intentional test"})
        self.assertEqual(state_path.read_bytes(), before)
        self.assertFalse(list(state_path.parent.glob(".session-*")))
        with mock.patch.object(d, "versions", return_value={}):
            with self.assertRaisesRegex(d.DeliveryError, "version changed"):
                d.session_status("learner")
        state_path.write_text("{")
        with self.assertRaisesRegex(d.DeliveryError, "Preserve"):
            d.session_status("learner")
        self.assertEqual(state_path.read_text(), "{")

    def test_reveal_does_not_count_as_independent_and_future_view_is_rejected(self):
        self.reach_transfer()
        with self.assertRaises(d.DeliveryError):
            self.act("evidence", {"view": "transfer.fields"}, "c02.inspect")
        self.act("reveal")
        self.act("predict", {"text": "Worked prediction after reveal."})
        self.act("continue")
        self.act("answer", {"text": "Observed fields."})
        self.act("continue")
        response = self.act("answer", {"text": "Worked calculation.", "answers": {"transfer.payload": "1160 bytes"}})
        self.assertFalse(response["result"]["checks"]["transfer.payload"]["independent"])
        self.experiment("c02.calculate")
        self.assertEqual(self.act("continue")["result"]["learning_result"], "demonstrated")

    def test_bad_session_paths_and_stale_requests(self):
        for name in ("../escape", "/tmp/escape", "a/b", "", "UPPER"):
            with self.assertRaises(d.DeliveryError):
                d.create_session(name)
        directory = d.session_dir("learner")
        (directory / "alias").symlink_to(directory / "packet-path.md")
        with self.assertRaises(d.DeliveryError):
            d.session_file(directory, "alias")
        request = self.request("skip", {"reason": "Test"})
        request["expected_revision"] += 1
        with self.assertRaisesRegex(d.DeliveryError, "Stale"):
            d.act("learner", request)

    def test_complete_day_both_case_assignments_and_staged_output(self):
        for letter in ("A", "B"):
            if letter == "B":
                self.view = d.create_session("reversed", case="B")
            ident = self.view["session_id"]
            visited = []
            while self.view["phase"]:
                phase = self.view["phase"]
                visited.append(phase["id"])
                if phase["id"] == "c04.choose":
                    self.assertNotIn("both transport paths use the same", phase["prompt"])
                    self.assertNotIn("failures.jsonl", phase["prompt"])
                if phase["id"] == "c05.round1":
                    self.assertEqual([v["id"] for v in phase["evidence"]], ["incident.round1"])
                if phase["id"] in ("c06.receive", "exit.answer"):
                    assigned = ("B" if letter == "A" else "A") if phase["block"] == "exit" else letter
                    self.assertTrue(phase["initial_diagnosis_required"])
                    self.assertEqual(phase["evidence"], [])
                    self.assertEqual(phase["checkpoints"], [])
                    self.assertNotIn("prefix was removed", phase["prompt"])
                    self.assertNotIn(f"case-{('B' if assigned == 'A' else 'A').lower()}.json", phase["prompt"])
                    request = dict(request_id=f"diagnosis-{self.view['revision']}", expected_revision=self.view["revision"], phase_id=phase["id"], action="diagnose", payload=DIAGNOSIS)
                    self.view = d.act(ident, request)
                    phase = self.view["phase"]
                if phase["kind"] in ("prediction", "reflection", "checkpoint"):
                    action = "answer"
                    payload = dict(text="Scripted rehearsal response; claims need human review.", answers=answers_for(phase, letter))
                elif phase["kind"] == "feedback":
                    action, payload = "feedback", {"wanted_to_know": 4, "manageable": 4}
                else:
                    action, payload = "continue", {}
                request = dict(request_id=f"run-{self.view['revision']}", expected_revision=self.view["revision"], phase_id=phase["id"], action=action, payload=payload)
                self.view = d.act(ident, request)
                if action != "continue":
                    self.assertNotEqual(self.view["result"].get("learning_result"), "incorrect")
                    if phase["id"] in EXPERIMENTS:
                        for operation, values in [("experiment_predict", dict(parameters=EXPERIMENTS[phase["id"]], prediction="Synthetic decision prediction")), ("experiment_result", {})]:
                            if operation == "experiment_result":
                                values = {"experiment_id": self.view["result"]["experiment"]["id"]}
                            self.view = d.act(ident, dict(request_id=f"experiment-{self.view['revision']}", expected_revision=self.view["revision"], phase_id=phase["id"], action=operation, payload=values))
                    request = dict(request_id=f"run-{self.view['revision']}", expected_revision=self.view["revision"], phase_id=phase["id"], action="continue", payload={})
                    self.view = d.act(ident, request)
            self.assertEqual(len(visited), len(d.definition()["phases"]))
            self.assertTrue(self.view["completion"]["delivery_finished"])
            self.assertTrue(self.view["completion"]["objective_checks_satisfied"])
            self.assertFalse(self.view["completion"]["self_reviewed_completion"])
            old = d.session_status(ident, "c06.review")
            request = dict(request_id="main-reveal", expected_revision=old["revision"], phase_id="c06.review", action="reveal", payload={})
            review = d.act(ident, request)["result"]["text"]
            self.assertIn(f"Case {letter}-v1", review)
            self.assertNotIn(f"Case {'B' if letter == 'A' else 'A'}-v1", review)

    def test_terminal_saves_an_answer_and_can_quit_without_advancing(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with mock.patch("sys.stdin.isatty", return_value=True), mock.patch("sys.stdout.isatty", return_value=True):
                with mock.patch("builtins.input", side_effect=("a", "My first prediction.", "q")):
                    self.assertEqual(d.learn("learner"), 0)
        resumed = d.session_status("learner")
        self.assertEqual(resumed["phase"]["id"], "opening.predict")
        self.assertEqual(resumed["phase"]["progress"]["submissions"][0]["text"], "My first prediction.")
        self.assertIn("Resume with ./course learn", output.getvalue())

    def test_artifacts_review_revisions_staleness_and_private_exports(self):
        self.finish_day()
        self.assertFalse(self.view["completion"]["required_work_recorded"])
        blank = self.review("c01.review")
        self.assertEqual(blank["result"]["learning_result"], "needs_revision")
        self.assertTrue(blank["result"]["artifact_check"]["errors"])
        directory = d.session_dir("learner")
        fill_rehearsal_artifacts(directory)
        self.review("c01.review", score=0)
        for phase in [p["id"] for p in d.definition()["phases"] if p["kind"] == "review"]:
            self.review(phase)
        status = d.session_status("learner")
        self.assertTrue(status["completion"]["self_reviewed_completion"])
        self.assertFalse(status["completion"]["facilitator_reviewed_completion"])
        for phase in [p["id"] for p in d.definition()["phases"] if p["kind"] == "review"]:
            self.review(phase, reviewer="facilitator")
        self.assertTrue(d.session_status("learner")["completion"]["facilitator_reviewed_completion"])
        summary = d.export_session("learner")
        self.assertNotIn("PRIVATE REHEARSAL TEXT", json.dumps(summary))
        self.assertEqual(len(summary["review_history"]["c01.review"]), 4)
        bundle = d.export_session("learner", True)
        self.assertIn("PRIVATE REHEARSAL TEXT", json.dumps(bundle))
        self.assertEqual(set(bundle["included_files"]), set(d.ARTIFACTS))
        csv_rows = list(csv.DictReader(io.StringIO(d.format_export(summary, "csv"))))
        self.assertEqual(len(csv_rows), len(d.definition()["phases"]))
        self.assertIn("# Course Review: learner", d.format_export(bundle, "markdown"))
        hashes = d.session_status("learner", "c01.review")["phase"]["artifact_hashes"]
        path = directory / "packet-path.md"
        path.write_text(path.read_text() + "\nUnrelated file note.\n")
        self.assertTrue(d.session_status("learner")["completion"]["self_reviewed_completion"])
        path.write_text(path.read_text().replace("<!-- artifact:end c01 -->", "Revised assessed region.\n<!-- artifact:end c01 -->"))
        stale = d.session_status("learner")
        self.assertFalse(stale["completion"]["self_reviewed_completion"])
        self.assertEqual(stale["reviews"]["c01.review"]["self"]["status"], "stale")
        with self.assertRaisesRegex(d.DeliveryError, "Artifact versions"):
            self.review("c01.review", hashes=hashes)

    def test_ledger_references_timestamps_and_narrative_limits(self):
        self.finish_day()
        directory = d.session_dir("learner")
        fill_rehearsal_artifacts(directory)
        state = d.load_state(directory, d.definition())
        phase = d.phase_by_id(d.definition(), "c05.review")
        self.assertTrue(d.validate_artifacts(directory, phase, state)["valid"])
        ledger = (directory / "evidence-ledger.csv").read_text()
        for changed in (ledger.replace("incident/flows.jsonl#1", "incident/flows.jsonl#99"),
                        ledger.replace("observed", "proven-attack"),
                        ledger.replace("2026-08-15", "2027-08-15"),
                        ledger.replace("evidence_id,source", "id,source")):
            self.assertTrue(d.ledger_errors(changed, state))
        path = directory / "incident.md"
        text = path.read_text()
        path.write_text(re.sub(r"(?<=<!-- narrative:start -->\n).*?(?=\n<!-- narrative:end -->)", "word " * 151, text, flags=re.S))
        self.assertTrue(any("1–150" in error for error in d.validate_artifacts(directory, phase, state)["errors"]))
        packet = directory / "packet-path.md"
        packet.write_text("# Sheet\n\n## Healthy Path — Challenge 1\n\nAn arbitrary sentence.\n")
        report = d.validate_artifacts(directory, d.phase_by_id(d.definition(), "c01.review"), state)
        self.assertFalse(report["valid"])
        self.assertTrue(any("table" in error for error in report["errors"]))

    def test_concurrent_requests_advance_only_once(self):
        script = "import sys; from pathlib import Path; import delivery; delivery.WORK_ROOT=Path(sys.argv[1]); raise SystemExit(delivery.cli(sys.argv[2:]))"
        arguments = [sys.executable, "-B", "-c", script, str(d.WORK_ROOT), "session", "act", "--id", "learner", "--input", "-", "--json"]
        request = self.request("skip", {"reason": "Concurrency rehearsal"})
        processes = [subprocess.Popen(arguments, cwd=d.ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
        for index, process in enumerate(processes):
            process.stdin.write(json.dumps({**request, "request_id": f"parallel-{index}"}))
            process.stdin.close()
            process.stdin = None
        codes = []
        for process in processes:
            stdout, stderr = process.communicate(timeout=10)
            codes.append(process.returncode)
            self.assertIn(json.loads(stdout)["status"], ("ok", "error"))
            self.assertEqual(stderr, "")
        self.assertEqual(sorted(codes), [0, 3])
        self.assertEqual(d.session_status("learner")["revision"], 1)

    def test_evidence_failure_and_injection_leave_state_unchanged(self):
        self.reach_transfer()
        self.act("predict", {"text": "First explanation."})
        self.act("continue")
        path = d.session_dir("learner") / "session.json"
        before = path.read_bytes()
        for result in (dict(returncode=7, truncated=False), dict(returncode=None, truncated=False, timed_out=True), dict(returncode=0, truncated=True)):
            with mock.patch.object(d, "run_tool", return_value=result):
                with self.assertRaises(d.DeliveryError) as error:
                    self.act("evidence", {"view": "transfer.fields"})
                self.assertEqual(error.exception.code, 4)
                self.assertEqual(error.exception.details, result)
            self.assertEqual(path.read_bytes(), before)
        with mock.patch.object(d, "run_tool") as run:
            with self.assertRaises(d.DeliveryError):
                self.act("evidence", {"view": "transfer.fields; touch unexpected"})
            run.assert_not_called()
        with mock.patch.object(d, "evidence_integrity", side_effect=d.DeliveryError("fixture checksum mismatch", 4)):
            with self.assertRaisesRegex(d.DeliveryError, "checksum"):
                self.act("answer", {"text": "Should not be saved."})
        self.assertEqual(path.read_bytes(), before)

    def test_export_files_do_not_overwrite_or_escape(self):
        command = ["session", "export", "--id", "learner", "--json", "--output", "summary.json"]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(d.cli(command), 0)
        self.assertEqual(json.loads(output.getvalue())["included_files"], [])
        target = d.session_dir("learner") / "exports/summary.json"
        before = target.read_bytes()
        for args, expected in ((command, 4), (command[:-1] + ["../escape.json"], 2),
                               (["session", "export", "--id", "learner", "--json", "--format", "csv"], 2)):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(d.cli(args), expected)
            self.assertEqual(json.loads(output.getvalue())["status"], "error")
        self.assertEqual(target.read_bytes(), before)
        self.assertFalse((d.session_dir("learner") / "escape.json").exists())

    def test_corrupt_valid_json_reports_recovery_without_reset(self):
        path = d.session_dir("learner") / "session.json"
        state = json.loads(path.read_text())
        state["phases"]["opening.predict"]["reviews"] = [{}]
        path.write_text(json.dumps(state))
        before = path.read_bytes()
        with self.assertRaisesRegex(d.DeliveryError, "Preserve this directory"):
            d.session_status("learner")
        self.assertEqual(path.read_bytes(), before)


class HeadlessTests(unittest.TestCase):
    def test_json_help_and_duplicate_keys(self):
        result = subprocess.run([sys.executable, "-B", str(d.ROOT / "course.py"), "session", "act", "--help", "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--input", json.loads(result.stdout)["help"])
        for text in ('{"revision": 0, "revision": 1}', '{"value": NaN}'):
            with self.assertRaises(d.DeliveryError):
                d.decode_json(text)

    def test_json_errors_without_terminal_input(self):
        for argv in (
            ["--json", "unknown"],
            ["session", "status", "--json"],
            ["session", "unknown", "--json"],
            ["session", "act", "--id", "unused", "--input", "-", "--json"],
        ):
            result = subprocess.run([sys.executable, "-B", str(d.ROOT / "course.py"), *argv],
                                    input="{", text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "error")
            self.assertEqual(result.stderr, "")

    def test_tool_failure_timeout_and_output_limit(self):
        result = d.run_tool([sys.executable, "-c", "raise SystemExit(7)"])
        self.assertEqual(result["returncode"], 7)
        result = d.run_tool([sys.executable, "-c", "import time; time.sleep(2)"], timeout=0.02)
        self.assertTrue(result["timed_out"])
        with mock.patch.object(d, "OUTPUT_LIMIT", 10):
            result = d.run_tool([sys.executable, "-c", "print('a' * 20)"])
        self.assertTrue(result["truncated"])
        self.assertEqual(len(result["stdout"]), 10)


if __name__ == "__main__":
    unittest.main()
