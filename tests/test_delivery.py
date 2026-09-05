"""Contracts and journeys for local course delivery."""

import copy
import contextlib
import io
import json
import shlex
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


def answers_for(phase, main_case):
    letter = ("B" if main_case == "A" else "A") if phase["block"] == "exit" else main_case
    answers = {**ANSWERS, "case.id": f"{letter}-v1", "case.change": "10.20.0.0/16" if letter == "A" else "ISOLATED",
               "case.lookup": "no route", "case.observation": "A3" if letter == "A" else "B2"}
    return {item["id"]: answers[item["id"]] for item in phase["checkpoints"]}


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

    def reach_transfer(self):
        while self.view["phase"]["id"] != "c02.predict":
            self.act("skip", {"reason": "Test setup for transfer slice"})

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
        self.assertTrue(resumed["phase"]["progress"]["checks"]["transfer.payload"]["independent"])
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
                    command = phase["evidence"][0]["command"]
                    self.assertIn(f"case-{assigned.lower()}.json", command)
                    self.assertTrue(any(shlex.split(line) == shlex.split(command)
                                        for line in phase["prompt"].splitlines() if line.startswith("jq ")))
                    self.assertNotIn(f"case-{('B' if assigned == 'A' else 'A').lower()}.json", phase["prompt"])
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
                    request = dict(request_id=f"run-{self.view['revision']}", expected_revision=self.view["revision"], phase_id=phase["id"], action="continue", payload={})
                    self.view = d.act(ident, request)
            self.assertEqual(len(visited), 36)
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


class HeadlessTests(unittest.TestCase):
    def test_json_errors_without_terminal_input(self):
        for argv in (
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
