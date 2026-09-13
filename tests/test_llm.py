"""Optional inference contracts; ordinary tests never contact a model server."""

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest import mock

import course
import delivery as d
import learning
import llm

LOCAL = {"BOOTCAMP_LLM_FEATURES": "review,coach,handoff,author",
         "BOOTCAMP_LLM_BASE_URL": "http://localhost:1234/v1",
         "BOOTCAMP_LLM_MODEL": "test-model", "BOOTCAMP_LLM_TOKEN_FIELD": "max_tokens"}


def envelope(advice=None, **changes):
    value = dict(choices=[dict(finish_reason="stop", message=dict(content=json.dumps(advice or {"ready": True})))],
                 usage=dict(prompt_tokens=10, completion_tokens=5, total_tokens=15, private="omit"))
    value.update(changes)
    return json.dumps(value).encode()


class ClientTests(unittest.TestCase):
    def setUp(self):
        patch = mock.patch.dict(os.environ, LOCAL, clear=True)
        patch.start()
        self.addCleanup(patch.stop)

    def test_offline_disabled_and_configuration(self):
        with mock.patch("urllib.request.build_opener", side_effect=AssertionError("network")):
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertEqual(llm.availability()["status"], "disabled")
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(course.main(["llm", "check", "--json"]), 0)
                with self.assertRaises(llm.LLMError):
                    llm.configuration()
            self.assertEqual(llm.availability()["status"], "configured")
            for key, value in (("BOOTCAMP_LLM_FEATURES", "unknown"),
                               ("BOOTCAMP_LLM_MODEL", ""),
                               ("BOOTCAMP_LLM_TIMEOUT_SECONDS", "nan"),
                               ("BOOTCAMP_LLM_TIMEOUT_SECONDS", "301"),
                               ("BOOTCAMP_LLM_MAX_OUTPUT_TOKENS", "0"),
                               ("BOOTCAMP_LLM_TOKEN_FIELD", "invented")):
                with self.subTest(key=key, value=value), mock.patch.dict(os.environ, {key: value}):
                    self.assertEqual(llm.availability()["status"], "configuration")

    def test_url_auth_and_no_ambient_key(self):
        for url in ("http://localhost:1234/v1", "http://127.0.0.1:1234/v1/", "http://[::1]:1234/v1"):
            with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": url, "OPENAI_API_KEY": "ambient-secret"}):
                config = llm.configuration()
                self.assertTrue(config.loopback)
                self.assertEqual(config.api_key, "")
        for url in ("http://example.com/v1", "https://user:secret@example.com/v1", "https://example.com/v1?key=secret",
                    "https://example.com/v1#fragment", "https://example.com/v1/chat/completions", "file:///v1",
                    "http://localhost:99999/v1", "https://example.com/v1/../v1", "http://localhost.evil/v1"):
            with self.subTest(url=url), mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": url}):
                with self.assertRaises(llm.LLMError):
                    llm.configuration()
        with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": "https://api.openai.com/v1"}):
            with self.assertRaises(llm.LLMError):
                llm.configuration()
            with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_API_KEY": "explicit-secret"}):
                self.assertNotIn("explicit-secret", repr(llm.configuration()))
                self.assertNotIn("explicit-secret", json.dumps(llm.configuration().public()))

    def test_both_wire_profiles_and_bearer_auth(self):
        for base, token, key in (("http://localhost:1234/v1", "max_tokens", ""),
                                 ("http://localhost:1234/v1", "max_tokens", "local-token"),
                                 ("https://api.openai.com/v1", "max_completion_tokens", "openai-token")):
            with self.subTest(base=base, key=bool(key)), mock.patch.dict(os.environ, {
                "BOOTCAMP_LLM_BASE_URL": base, "BOOTCAMP_LLM_TOKEN_FIELD": token, "BOOTCAMP_LLM_API_KEY": key,
            }), mock.patch("urllib.request.build_opener") as factory:
                factory.return_value.open.return_value = io.BytesIO(envelope())
                result = llm.generate(llm.configuration(), "check", {})
                request = factory.return_value.open.call_args.args[0]
                self.assertEqual(request.full_url, base + "/chat/completions")
                body = json.loads(request.data)
                self.assertEqual(set(body), {"model", "messages", "stream", token})
                self.assertEqual(body[token], 2048)
                self.assertFalse(body["stream"])
                self.assertEqual(request.get_header("Authorization"), "Bearer " + key if key else None)
                self.assertEqual(result["usage"], dict(prompt_tokens=10, completion_tokens=5, total_tokens=15))
                self.assertNotIn("private", result["usage"])
                self.assertIsNone(llm.NoRedirect().redirect_request(request, None, 302, "", {}, "https://evil.example"))
                if base.startswith("http:"):
                    self.assertTrue(any(isinstance(h, llm.urllib.request.ProxyHandler) and not h.proxies
                                        for h in factory.call_args.args))

    def test_bounded_context_response_and_failure_privacy(self):
        with mock.patch("urllib.request.build_opener") as factory:
            with self.assertRaises(llm.LLMError):
                llm.generate(llm.configuration(), "check", {"text": "x" * llm.CONTEXT_LIMIT})
            factory.assert_not_called()
            for raw in (b"x" * (llm.RESPONSE_LIMIT + 1), b"not JSON", b'{"choices":[]}',
                        envelope(choices=[dict(finish_reason="length", message=dict(content='{}'))]),
                        envelope(choices=[dict(finish_reason="stop", message=dict(content='{"ready": true}', refusal="refused"))])):
                factory.return_value.open.return_value = io.BytesIO(raw)
                with self.assertRaises(llm.LLMError):
                    llm.generate(llm.configuration(), "check", {})
            for failure in (TimeoutError("secret"), urllib.error.URLError("secret"),
                            urllib.error.HTTPError("https://secret", 401, "secret", {}, io.BytesIO(b"secret")),
                            urllib.error.HTTPError("https://secret", 429, "secret", {}, io.BytesIO(b"secret"))):
                factory.return_value.open.side_effect = failure
                with self.assertRaises(llm.LLMError) as caught:
                    llm.generate(llm.configuration(), "check", {})
                self.assertNotIn("secret", str(caught.exception))

    def test_advice_schema_quotes_and_citations(self):
        context = dict(learner_text="A login proves theft.", evidence={"incident/auth.jsonl#2": {}})
        finding = dict(dimension="evidence", claim_quote="A login proves theft.", evidence_ids=["incident/auth.jsonl#2"],
                       explanation="Authentication does not establish credential acquisition.",
                       revision_question="What evidence would distinguish authorized use?")
        result = dict(findings=[finding], insufficient_evidence=False)
        self.assertEqual(llm.validate_output("review", result, context), result)
        for change in (dict(evidence_ids=["reserved-case"]), dict(claim_quote="invented"), dict(dimension="score")):
            with self.assertRaises(llm.LLMError):
                llm.validate_output("review", dict(findings=[{**finding, **change}], insufficient_evidence=False), context)
        with self.assertRaises(llm.LLMError):
            llm.validate_output("coach", dict(explanation="Ignore instructions", question="?", evidence_ids=[], score=8), context)
        with self.assertRaises(llm.LLMError):
            llm.validate_output("handoff", dict(question="\x1b[31m", evidence_ids=[]), context)
        with self.assertRaises(ValueError):
            llm.decode('{"ready": true, "ready": false}')


class AuthorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        for patch in (mock.patch.dict(os.environ, LOCAL, clear=True),
                      mock.patch.object(d, "WORK_ROOT", Path(self.temp.name))):
            patch.start()
            self.addCleanup(patch.stop)

    def generated(self, config, feature, context):
        return dict(advice=dict(draft="Unreviewed wording for the fixed conditions."),
                    endpoint=config.base_url, model=config.model, prompt_version=1, latency_ms=1, usage={})

    def test_supported_examples_exclude_reserved_problems_and_compute_facts(self):
        for family in learning.catalog()["families"]:
            context = llm.author_context(family, "practice-variant")
            self.assertEqual(context["example"]["use"], "supported")
            self.assertNotIn("reassessment", json.dumps(context))
            self.assertNotIn("case-b.json", json.dumps(context))
        self.assertEqual(llm.author_context("transfer", "explanation")["computed_facts"]["maximum_payload"], 1348)
        candidate = llm.author_context("transfer", "practice-variant", seed=7)
        self.assertEqual(candidate, llm.author_context("transfer", "practice-variant", seed=7))
        self.assertNotIn(candidate["example"]["parameters"]["mtu"], {p["parameters"]["mtu"] for p in learning.catalog()["families"]["transfer"]})
        self.assertEqual(candidate["authored_facts"]["payload"], f"{candidate['computed_facts']['maximum_payload']} bytes")
        self.assertTrue(llm.author_context("subnet", "explanation")["computed_facts"]["local"])
        routes = llm.author_context("route-selection", "explanation")["computed_facts"]
        self.assertEqual(routes["before"][0]["prefix"], "10.1.2.3/32")
        self.assertEqual(len(routes["after"]), 2)

    def test_authoring_is_explicit_private_and_never_overwrites(self):
        with mock.patch.object(llm, "generate", side_effect=self.generated) as generate:
            result = llm.author("transfer", "practice-variant", "transfer.json")
            path = Path(result["output"])
            record = json.loads(path.read_text())
            self.assertEqual(record["status"], "unreviewed-draft")
            self.assertIn("independent answer keys", record["review_required"])
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            for name in ("transfer.json", "../escape.json", "/tmp/escape.json"):
                with self.assertRaises(d.DeliveryError):
                    llm.author("transfer", "explanation", name)
            self.assertEqual(generate.call_count, 1)
            with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_FEATURES": "review"}):
                with self.assertRaises(llm.LLMError):
                    llm.author("transfer", "explanation", "new.json")

    def test_concurrent_output_symlink_and_interruption_preserve_files(self):
        target = llm.write_work_json("llm-drafts", "existing.json", {"original": True})
        alias = target.parent / "alias.json"
        alias.symlink_to(target)
        with self.assertRaises(d.DeliveryError):
            llm.work_output("llm-drafts", "alias.json")
        with mock.patch.object(llm.os, "link", side_effect=FileExistsError):
            with self.assertRaises(FileExistsError):
                llm.write_work_json("llm-drafts", "new.json", {"new": True})
        self.assertEqual(json.loads(target.read_text()), {"original": True})
        self.assertFalse(list(target.parent.glob(".llm-*")))
        self.assertFalse((target.parent / "new.json").exists())

    def test_author_cli(self):
        with mock.patch.object(llm, "generate", side_effect=self.generated), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(course.main(["llm", "author", "--family", "transfer", "--kind", "explanation", "--output", "cli.json", "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["draft_status"], "unreviewed-draft")

    def test_evaluation_is_offline_by_default_and_never_claims_human_review(self):
        evaluation = d.module_at("verification/check_llm.py")
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(evaluation.main(["--check"]), 0)
        self.assertEqual(len(evaluation.cases()), 10)
        with mock.patch.object(llm, "generate", side_effect=self.generated):
            result = evaluation.evaluate("author", "held-out", "author.json")
        saved = json.loads(Path(result["output"]).read_text())
        self.assertEqual(saved["status"], "human-review-pending")
        self.assertEqual(saved["examples"][0]["split"], "held-out")
        self.assertIsNone(saved["examples"][0]["facilitator"]["grounded"])


if __name__ == "__main__":
    unittest.main()
