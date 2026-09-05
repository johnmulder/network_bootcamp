"""Contracts and journeys for local course delivery."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import delivery as d


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
