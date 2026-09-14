"""Advisory session behavior, release boundaries, and durable help exposure."""

import contextlib
import io
import json
import os
import unittest
from unittest import mock

import course
import delivery as d
import llm
import llm_delivery as support
import test_delivery as fixtures
from test_llm import FAKE_KEY, LOCAL, credential_echo, envelope


class AdvisoryTests(unittest.TestCase):
    request = fixtures.SessionTests.request
    act = fixtures.SessionTests.act
    experiment = fixtures.SessionTests.experiment

    def setUp(self):
        settings = mock.patch.dict(os.environ, LOCAL, clear=True)
        settings.start()
        self.addCleanup(settings.stop)
        fixtures.SessionTests.setUp(self)

    def reach(self, phase):
        while self.view["phase"]["id"] != phase:
            self.act("skip", dict(reason="Synthetic LLM test setup"))

    def generated(self, config, feature, context):
        if feature == "review":
            advice = dict(findings=[dict(dimension="uncertainty", claim_quote="PRIVATE REHEARSAL TEXT",
                                        evidence_ids=["incident/auth.jsonl#2"],
                                        explanation="A login does not establish credential theft.",
                                        revision_question="What evidence would distinguish authorized use?")], insufficient_evidence=False)
        elif feature == "coach":
            advice = dict(explanation="Consider both headers in the stated bound.",
                          question="Which header did your calculation include?", evidence_ids=[])
        else:
            advice = dict(question="Who owns the next check and how will it be validated?", evidence_ids=[])
        return dict(advice=advice, model=config.model, endpoint=config.base_url,
                    prompt_version=llm.PROMPT_VERSION, usage={}, latency_ms=1)

    def open_view(self, phase, view):
        command = d.evidence_command(view, dict(case="A"))
        source = next(arg for arg in command if arg.startswith("labs/fixtures/"))
        value = (d.ROOT / source).read_text()
        if view.startswith("case.main."):
            packet = json.loads(value)
            keys = {"state": ("before", "after", "routes", "flow"), "observations": ("observations",),
                    "conditions": ("conditions", "limitations", "path", "scope")}[view.rsplit(".", 1)[1]]
            value = json.dumps({key: packet[key] for key in keys})
        with mock.patch.object(d, "run_tool", return_value=dict(returncode=0, truncated=False, stdout=value)):
            self.act("evidence", dict(view=view), phase)

    def prepare_review(self):
        self.reach("c05.narrative")
        fixtures.fill_rehearsal_artifacts(d.session_dir("learner"))
        for number in (1, 2, 3):
            self.open_view(f"c05.round{number}", f"incident.round{number}")
        self.act("answer", dict(text="PRIVATE submitted narrative"))
        self.act("continue")

    def prepare_coach(self, correct=False):
        self.reach("c02.calculate")
        self.act("answer", dict(text="PRIVATE calculation", answers={"transfer.payload": "1160 bytes" if correct else "1200 bytes"}))

    def test_review_context_citations_snapshots_and_private_export(self):
        self.prepare_review()
        before = d.export_session("learner")["completion"]
        with mock.patch.object(llm, "generate", side_effect=self.generated) as generate:
            request = self.request("llm_review")
            result = d.act("learner", request)
            context = generate.call_args.args[2]
            self.assertIn("incident/auth.jsonl#2", context["evidence"])
            self.assertNotIn("c06-handoff", context["regions"])
            self.assertNotIn("B-v1", json.dumps(context))
            self.assertNotIn("transfer-r1", json.dumps(context))
            self.assertEqual(result["result"]["learning_result"], "advisory_complete")
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertEqual(d.act("learner", request), result)
            self.assertEqual(generate.call_count, 1)
        self.assertEqual(d.export_session("learner")["completion"], before)
        public = json.dumps(d.export_session("learner"))
        self.assertNotIn("PRIVATE", public)
        self.assertNotIn("distinguish authorized", public)
        private = d.export_session("learner", True)
        self.assertIn("distinguish authorized", json.dumps(private))
        self.assertIn("distinguish authorized", d.format_export(private, "markdown"))
        self.assertFalse(d.load_state(d.session_dir("learner"), d.definition())["phases"]["c05.review"]["reviews"])

    def test_help_exposes_assigned_variant_but_preserves_independent_original(self):
        self.prepare_coach(correct=True)
        self.act("reassess", dict(family="transfer"))
        with mock.patch.object(llm, "generate", side_effect=self.generated):
            result = self.act("llm_coach", dict(family="transfer"))
        self.assertTrue(result["phase"]["progress"]["checks"]["transfer.payload"]["independent"])
        state = d.load_state(d.session_dir("learner"), d.definition())
        self.assertTrue(state["learning"][0]["exposed"])
        self.assertNotIn("m1.routes.10.0.20.40", state["phases"]["c01.change"]["exposed_checks"])
        exposed = state["learning"][0]["variant_id"]
        answers = {q["id"]: q["answer"] for q in d.learning.find_problem(exposed)["questions"]}
        result = self.act("problem_answer", dict(variant_id=exposed, answers=answers))
        self.assertFalse(result["result"]["problem_result"]["independent"])
        result = self.act("reassess", dict(family="transfer"))
        fresh = result["result"]["problem_result"]["id"]
        answers = {q["id"]: q["answer"] for q in d.learning.find_problem(fresh)["questions"]}
        result = self.act("problem_answer", dict(variant_id=fresh, answers=answers))
        self.assertTrue(result["result"]["problem_result"]["independent"])

    def test_pending_duplicate_interruption_and_cancel_with_feature_disabled(self):
        self.prepare_coach()
        request = self.request("llm_coach", dict(family="transfer"))
        with mock.patch.object(llm, "generate", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                d.act("learner", request)
        with mock.patch.object(llm, "generate", side_effect=AssertionError("duplicate inference")):
            self.assertEqual(d.act("learner", request)["result"]["learning_result"], "advisory_pending")
            with self.assertRaises(d.DeliveryError):
                self.act("llm_coach", dict(family="transfer"))
            with self.assertRaises(d.DeliveryError):
                d.act("learner", {**request, "action": "skip", "payload": {"reason": "ID collision"}})
            with mock.patch.dict(os.environ, {}, clear=True):
                self.act("llm_cancel", dict(request_id=request["request_id"]))
            self.assertEqual(d.act("learner", request)["result"]["learning_result"], "advisory_cancelled")
        self.assertFalse(d.session_status("learner")["phase"]["progress"]["exposed"])

    def test_terminal_recovers_pending_requests_without_valid_configuration(self):
        self.prepare_coach(correct=True)
        before = d.session_status("learner")["phase"]["progress"]
        for settings in ({}, {**LOCAL, "BOOTCAMP_LLM_BASE_URL": "invalid"}):
            with self.subTest(settings=settings):
                request = self.request("llm_coach", dict(family="transfer"), "c02.calculate")
                with mock.patch.object(llm, "generate", side_effect=KeyboardInterrupt):
                    with self.assertRaises(KeyboardInterrupt):
                        d.act("learner", request)
                with mock.patch.dict(os.environ, settings, clear=True), \
                        mock.patch("urllib.request.build_opener", side_effect=AssertionError("network")):
                    with contextlib.redirect_stdout(io.StringIO()) as output, \
                            mock.patch.object(d.sys.stdin, "isatty", return_value=True), \
                            mock.patch.object(d.sys.stdout, "isatty", return_value=True), \
                            mock.patch("builtins.input", side_effect=["s", "Offline recovery regression", "q"]):
                        self.assertEqual(d.learn("learner"), 0)
                    self.assertIn("Recover with ./course llm cancel", output.getvalue())
                    self.assertNotIn("Optional LLM:", output.getvalue())
                    self.act("llm_cancel", dict(request_id=request["request_id"]))
                    state = d.load_state(d.session_dir("learner"), d.definition())
                    self.assertEqual(state["llm_requests"][request["request_id"]]["status"], "cancelled")
                    self.assertIn("Offline recovery regression", (d.session_dir("learner") / "session.json").read_text())
                    progress = state["phases"]["c02.calculate"]
                    for key in ("submissions", "checks", "exposed", "exposed_checks"):
                        self.assertEqual(progress[key], before[key])

    def test_inference_releases_lock_and_discards_concurrent_changes(self):
        self.prepare_coach()
        request = self.request("llm_coach", dict(family="transfer"))

        def change(config, feature, context):
            self.assertEqual(d.act("learner", request)["result"]["learning_result"], "advisory_pending")
            self.act("answer", dict(text="A concurrent correction", answers={"transfer.payload": "1160 bytes"}))
            return self.generated(config, feature, context)

        with mock.patch.object(llm, "generate", side_effect=change):
            result = d.act("learner", request)
        self.assertEqual(result["result"]["learning_result"], "advisory_stale")
        self.assertNotIn("advice", result["result"])
        self.assertFalse(result["phase"]["progress"]["exposed"])

    def test_artifact_edits_make_pending_advice_stale(self):
        self.prepare_review()

        def change(config, feature, context):
            path = d.session_dir("learner") / "incident.md"
            path.write_text(path.read_text().replace("PRIVATE REHEARSAL TEXT", "Edited narrative"))
            return self.generated(config, feature, context)

        with mock.patch.object(llm, "generate", side_effect=change):
            result = self.act("llm_review")
        self.assertEqual(result["result"]["learning_result"], "advisory_stale")
        self.assertFalse(result["phase"]["progress"]["exposed"])

    def test_failure_preserves_assessment_and_can_resume_without_config(self):
        self.prepare_coach()
        with mock.patch.object(llm, "generate", side_effect=llm.LLMError("Unavailable", "unavailable")):
            result = self.act("llm_coach", dict(family="transfer"))
        self.assertEqual(result["result"]["learning_result"], "advisory_failed")
        self.assertFalse(result["phase"]["progress"]["exposed"])
        with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": "broken"}):
            self.assertEqual(d.session_status("learner")["llm"]["configuration"]["status"], "configuration")
            self.act("answer", dict(text="Correction", answers={"transfer.payload": "1160 bytes"}))

    def test_decoded_credential_failure_is_private_and_durable(self):
        self.prepare_coach(correct=True)
        request = self.request("llm_coach", dict(family="transfer"))
        before = d.session_status("learner")["phase"]["progress"]
        advice = dict(explanation=FAKE_KEY, question="What next?", evidence_ids=[])
        with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_API_KEY": FAKE_KEY}), \
                mock.patch("urllib.request.build_opener") as factory:
            factory.return_value.open.return_value = io.BytesIO(credential_echo(advice))
            result = d.act("learner", request)
            self.assertEqual(result["result"]["learning_result"], "advisory_failed")
            self.assertEqual(d.act("learner", request), result)
            factory.return_value.open.assert_called_once()
        state = d.load_state(d.session_dir("learner"), d.definition())
        entry = state["llm_requests"][request["request_id"]]
        self.assertEqual(entry["status"], "failed")
        self.assertEqual(entry["error_code"], "invalid-output")
        self.assertNotIn("advice", entry)
        self.assertEqual(d.session_status("learner")["phase"]["progress"], before)
        for text in (json.dumps(result), (d.session_dir("learner") / "session.json").read_text(),
                     json.dumps(d.export_session("learner")), json.dumps(d.export_session("learner", True))):
            self.assertNotIn(FAKE_KEY, text)

    def test_unicode_failure_replays_safely_and_valid_text_round_trips(self):
        self.prepare_coach(correct=True)
        before = d.session_status("learner")["phase"]["progress"]
        for text in ("\ud800", "\udfff", "Café 🚀"):
            with self.subTest(text=ascii(text)), mock.patch("urllib.request.build_opener") as factory:
                request = self.request("llm_coach", dict(family="transfer"))
                advice = dict(explanation=text, question="What next?", evidence_ids=[])
                factory.return_value.open.return_value = io.BytesIO(envelope(advice))
                result = d.act("learner", request)
                self.assertEqual(d.act("learner", request), result)
                factory.return_value.open.assert_called_once()
                state = d.load_state(d.session_dir("learner"), d.definition())
                entry = state["llm_requests"][request["request_id"]]
                if text == "Café 🚀":
                    self.assertEqual(result["result"]["learning_result"], "advisory_complete")
                    self.assertEqual(entry["advice"], advice)
                    exported = d.export_session("learner", True)
                    restored = json.loads(json.dumps(exported, ensure_ascii=False).encode("utf-8"))
                    self.assertEqual(restored["llm_history"][-1]["advice"], advice)
                else:
                    self.assertEqual(result["result"]["learning_result"], "advisory_failed")
                    self.assertEqual(entry["status"], "failed")
                    self.assertEqual(entry["error_code"], "invalid-output")
                    self.assertNotIn("advice", entry)
                    self.assertEqual(d.session_status("learner")["phase"]["progress"], before)

    def test_first_response_required_and_exit_always_excluded(self):
        self.reach("c02.calculate")
        before = (d.session_dir("learner") / "session.json").read_bytes()
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")):
            with self.assertRaises(d.DeliveryError):
                self.act("llm_coach", dict(family="transfer"))
            self.assertEqual((d.session_dir("learner") / "session.json").read_bytes(), before)
            with self.assertRaises(d.DeliveryError):
                self.act("llm_review", phase="exit.review")
        self.reach("exit.answer")
        self.assertFalse(any(a.startswith("llm_") for a in d.session_status("learner")["phase"]["allowed_actions"]))

    def test_input_budget_rejects_before_reservation_without_exposing_work(self):
        self.prepare_review()
        before = (d.session_dir("learner") / "session.json").read_bytes()
        with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_MAX_INPUT_BYTES": "1024"}), \
                mock.patch("urllib.request.build_opener", side_effect=AssertionError("network")):
            with self.assertRaisesRegex(d.DeliveryError, "configured limit is 1024"):
                self.act("llm_review")
        self.assertEqual((d.session_dir("learner") / "session.json").read_bytes(), before)

    def test_real_context_compacts_without_changing_evidence_or_saved_hashes(self):
        self.prepare_review()
        state = d.load_state(d.session_dir("learner"), d.definition())
        context, hashes = support.build_context(state, d.definition(), d.phase_by_id(d.definition(), "c05.review"), "review", {})
        before = support.context_hash(context)
        body, size = llm.prepare_request(llm.configuration(), "review", context)
        compact = json.loads(body["messages"][1]["content"])
        self.assertLess(len(llm.json_text(compact)), len(llm.json_text(context)))
        self.assertEqual(set(compact["evidence"]), set(context["evidence"]))
        self.assertEqual(compact["learner_text"], context["learner_text"])
        self.assertEqual(support.context_hash(context), before)
        self.assertEqual(hashes, d.review_hashes(d.session_dir("learner"), d.phase_by_id(d.definition(), "c05.review")))
        with mock.patch("urllib.request.build_opener") as factory:
            factory.return_value.open.return_value = io.BytesIO(envelope(self.generated(llm.configuration(), "review", context)["advice"]))
            request = self.request("llm_review")
            result = d.act("learner", request)
            self.assertEqual(d.act("learner", request), result)
            factory.return_value.open.assert_called_once()
        public = d.export_session("learner")["llm"]
        self.assertIn(str(size), json.dumps(public))

    def test_unopened_citations_do_not_fetch_more_evidence(self):
        self.prepare_review()
        state = d.load_state(d.session_dir("learner"), d.definition())
        state["phases"]["c05.round2"]["views"] = []
        d.save_state(d.session_dir("learner"), state)
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")):
            with self.assertRaisesRegex(d.DeliveryError, "Open the evidence views"):
                self.act("llm_review")
        phase = d.phase_by_id(d.definition(), "c05.round2")
        evidence = support.opened_evidence(state, d.definition(), phase)
        self.assertNotIn("view:incident.round3", evidence)
        self.assertNotIn("incident/auth.jsonl#2", evidence)

    def test_handoff_uses_only_opened_case_fields_and_limits_three_turns(self):
        self.reach("c06.receive")
        self.act("diagnose", fixtures.DIAGNOSIS)
        self.reach("c06.analyze")
        self.open_view("c06.analyze", "case.main.observations")
        self.act("answer", dict(text="PRIVATE analysis", answers=fixtures.answers_for(self.view["phase"], "A")))
        self.act("continue")
        fixtures.fill_rehearsal_artifacts(d.session_dir("learner"))
        self.act("answer", dict(text="PRIVATE handoff"))
        self.act("continue")
        with mock.patch.object(llm, "generate", side_effect=self.generated) as generate:
            with self.assertRaisesRegex(d.DeliveryError, "reply must be text"):
                self.act("llm_handoff", dict(role="security", text=[]))
            for index in range(3):
                self.act("llm_handoff", dict(role="network-operations", text="A recipient reply" if index else ""))
                self.assertEqual(support.learner_help("learner", "c06.exchange")["handoff_turns_remaining"], 2 - index)
            context = generate.call_args.args[2]
            self.assertNotIn("view:case.main.state", context["evidence"])
            self.assertNotIn("view:case.main.conditions", context["evidence"])
            self.assertEqual(len(context["exchange"]), 2)
            with self.assertRaisesRegex(d.DeliveryError, "three model turns"):
                self.act("llm_handoff", dict(role="security", text="One more"))
            path = d.session_dir("learner") / "incident.md"
            path.write_text(path.read_text().replace("PRIVATE REHEARSAL TEXT", "Revised PRIVATE REHEARSAL TEXT"))
            self.act("llm_handoff", dict(role="security", text=""))
            self.assertEqual(generate.call_count, 4)
            history = support.learner_help("learner", "c06.exchange")
            self.assertEqual(history["handoff_turns_remaining"], 2)
            self.assertEqual([entry["current"] for entry in history["entries"]], [False, False, False, True])

    def test_terminal_and_cli_share_the_session_action(self):
        self.prepare_coach()
        output = io.StringIO()
        with mock.patch.object(llm, "generate", side_effect=self.generated), contextlib.redirect_stdout(output):
            self.assertEqual(course.main(["llm", "coach", "--id", "learner", "--phase", "c02.calculate", "--family", "transfer", "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["result"]["learning_result"], "advisory_complete")
        with contextlib.redirect_stdout(io.StringIO()) as output, mock.patch.object(d.sys.stdin, "isatty", return_value=True), \
                mock.patch.object(d.sys.stdout, "isatty", return_value=True), \
                mock.patch("builtins.input", side_effect=["lc", "transfer", "q"]), \
                mock.patch.object(llm, "generate", side_effect=self.generated):
            self.assertEqual(d.learn("learner"), 0)
        self.assertIn("Which header", output.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(course.main(["llm", "coach", "--json"]), 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "error")

    def test_saved_advice_is_read_only_private_and_marks_revised_answers(self):
        self.prepare_coach()
        with mock.patch.object(llm, "generate", side_effect=self.generated):
            self.act("llm_coach", dict(family="transfer"))
        path = d.session_dir("learner") / "session.json"
        before = path.read_bytes()
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")):
            history = support.learner_help("learner", "c02.calculate")
            self.assertTrue(history["entries"][0]["current"])
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(course.main(["llm", "history", "--id", "learner", "--phase", "c02.calculate", "--json"]), 0)
            self.assertEqual(json.loads(output.getvalue())["entries"], history["entries"])
            self.assertEqual(path.read_bytes(), before)
            self.assertNotIn("Which header", json.dumps(d.export_session("learner")))
        self.act("answer", dict(text="I have revised my calculation.", answers={"transfer.payload": "1160 bytes"}))
        history = support.learner_help("learner", "c02.calculate")
        self.assertFalse(history["entries"][0]["current"])
        self.assertIn("Earlier work", llm.format_history(history))

    def test_readiness_and_plain_feedback_preserve_json_contract(self):
        self.reach("c02.calculate")
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")):
            help_view = support.learner_help("learner", "c02.calculate")
            self.assertIn("Commit an answer", help_view["readiness"][0]["reason"])
        self.act("answer", dict(text="My calculation", answers={"transfer.payload": "1200 bytes"}))
        with mock.patch.object(llm, "generate", side_effect=self.generated), \
                contextlib.redirect_stdout(io.StringIO()) as output, contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(course.main(["llm", "coach", "--id", "learner", "--phase", "c02.calculate", "--family", "transfer"]), 0)
        self.assertIn("Next step: Which header", output.getvalue())
        self.assertIn("Elapsed:", output.getvalue())
        self.assertNotIn('"advice":', output.getvalue())
        self.assertIn("server inference may continue", errors.getvalue())
        rendered = llm.format_advice("review", dict(findings=[], insufficient_evidence=True))
        self.assertIn("not a passing score", rendered)
        self.assertIn("could not fully assess", rendered)

    def test_terminal_rereads_without_inference_and_defaults_single_family(self):
        self.prepare_coach()
        with contextlib.redirect_stdout(io.StringIO()) as output, mock.patch.object(d.sys.stdin, "isatty", return_value=True), \
                mock.patch.object(d.sys.stdout, "isatty", return_value=True), \
                mock.patch("builtins.input", side_effect=["lc", "", "la", "q"]), \
                mock.patch.object(llm, "generate", side_effect=self.generated) as generate:
            self.assertEqual(d.learn("learner"), 0)
        self.assertEqual(generate.call_count, 1)
        self.assertEqual(output.getvalue().count("Next step: Which header"), 2)

    def test_plain_failure_gives_recovery_without_retry(self):
        self.prepare_coach()
        with mock.patch.object(llm, "generate", side_effect=llm.LLMError("Timed out", "unavailable")) as generate, \
                contextlib.redirect_stdout(io.StringIO()) as output, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(course.main(["llm", "coach", "--id", "learner", "--phase", "c02.calculate", "--family", "transfer"]), 4)
        self.assertEqual(generate.call_count, 1)
        self.assertIn("saved work is still available", output.getvalue())
        self.assertFalse(d.session_status("learner")["phase"]["progress"]["exposed"])

    def test_optional_settings_never_make_normal_delivery_contact_a_model(self):
        with mock.patch.object(llm, "generate", side_effect=AssertionError("inference")), \
                mock.patch("urllib.request.build_opener", side_effect=AssertionError("network")):
            for settings in ({}, {**LOCAL, "BOOTCAMP_LLM_FEATURES": ""},
                             {**LOCAL, "BOOTCAMP_LLM_BASE_URL": "invalid"}, LOCAL):
                with mock.patch.dict(os.environ, settings, clear=True):
                    d.session_status("learner")
                    d.export_session("learner")
                    self.act("skip", dict(reason="Offline configuration check"))
            fixtures.SessionTests.finish_day(self)
            self.assertTrue(d.session_status("learner")["completion"]["delivery_finished"])

    def test_session_evaluation_exercises_real_actions_with_mocked_transport(self):
        evaluation = d.module_at("verification/check_llm.py")

        def evidence(argv, **kwargs):
            source = next(arg for arg in argv if arg.startswith("labs/fixtures/"))
            return dict(returncode=0, truncated=False, stdout=(d.ROOT / source).read_text())

        def generate(config, feature, context):
            value = self.generated(config, feature, context)
            if feature == "review":
                value["advice"] = dict(findings=[], insufficient_evidence=True)
            return value

        with mock.patch.object(d, "run_tool", side_effect=evidence), \
                mock.patch.object(llm, "generate", side_effect=generate) as provider:
            result = evaluation.evaluate_session("session-evaluation.json", "Synthetic server")
            self.assertEqual(provider.call_count, 6)
        from pathlib import Path
        record = json.loads(Path(result["output"]).read_text())
        self.assertEqual(record["status"], "human-review-pending")
        self.assertTrue(record["budget_rejection_verified"])
        self.assertTrue(record["replay_verified"])
        self.assertEqual(len(record["examples"]), 6)


if __name__ == "__main__":
    unittest.main()
