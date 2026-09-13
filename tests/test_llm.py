"""Optional inference contracts; ordinary tests never contact a model server."""

import contextlib
import io
import json
import os
import unittest
import urllib.error
from unittest import mock

import course
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


if __name__ == "__main__":
    unittest.main()
