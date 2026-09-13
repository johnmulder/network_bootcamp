# Optional LLM Support

The course includes four experimental advisory features: rubric-based review,
adaptive explanations, a handoff practice partner, and maintainer drafting.
Each is disabled by default. After core prerequisites are installed, the
complete required course works offline with no model server, credentials,
or additional Python packages.

Only an explicit LLM action sends context to the configured endpoint. Setup,
normal submissions, status, exports, verification, and course packaging never
contact it. Static hints, worked examples, pair exchange, and self-review remain
available. An unavailable local model never triggers a fallback to OpenAI.

## Configure a server

Set these environment variables in the shell that launches `./course`.
Sessions record the configured model and endpoint as request provenance, but
do not serialize the API-key setting. Selected learner text and files are
not a general secret-redaction system; see the context and export rules below.

| Variable | Default | Meaning |
| --- | --- | --- |
| `BOOTCAMP_LLM_FEATURES` | Empty | Comma-separated subset of `review`, `coach`, `handoff`, `author`. |
| `BOOTCAMP_LLM_BASE_URL` | Unset | API root whose path is exactly `/v1`; HTTPS, or HTTP on loopback. |
| `BOOTCAMP_LLM_MODEL` | Unset | Exact model identifier available on that server. |
| `BOOTCAMP_LLM_API_KEY` | Unset | Endpoint-specific bearer token. OpenAI requires it; local authentication may be disabled. |
| `BOOTCAMP_LLM_TOKEN_FIELD` | `max_completion_tokens` | Set to `max_tokens` for the documented LM Studio profile. |
| `BOOTCAMP_LLM_RESPONSE_FORMAT` | `prompt` | `prompt` requests JSON in text instructions; `json_schema` also asks the server to enforce the advice schema. |
| `BOOTCAMP_LLM_MAX_OUTPUT_TOKENS` | `2048` | Integer output budget, 1–8192. |
| `BOOTCAMP_LLM_TIMEOUT_SECONDS` | `60` | Integer timeout for blocking network operations, 1–300 seconds; not a total elapsed-time limit. |

Trailing slashes are normalized. Custom prefixes such as `/proxy/v1`, a full
`/v1/chat/completions` URL, embedded credentials, query strings, and fragments
are rejected. HTTP requires `localhost` or a loopback IP literal; other hosts
require HTTPS. The selected model must be supplied explicitly.

The client sends text to `/v1/chat/completions` without streaming or tools.
Optional `json_schema` mode uses the shared Chat Completions response format;
the default `prompt` mode omits it. Both modes validate advice locally,
including exact quotes and citation IDs. An unsupported schema request fails
without retrying; explicitly select `prompt` for a server without support.
The two token-budget fields reflect the respective
[OpenAI](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
and [LM Studio](https://lmstudio.ai/docs/developer/openai-compat/chat-completions)
documentation. Compatibility and feedback quality depend on the selected model.

### OpenAI

Replace the model placeholder with an available Chat Completions model. The
example assumes `OPENAI_API_KEY` has already been provided securely; the
explicit assignment chooses that credential for this endpoint.

```sh
export BOOTCAMP_LLM_FEATURES=review
export BOOTCAMP_LLM_BASE_URL=https://api.openai.com/v1
export BOOTCAMP_LLM_MODEL='<your-openai-model-id>'
export BOOTCAMP_LLM_API_KEY="$OPENAI_API_KEY"
export BOOTCAMP_LLM_TOKEN_FIELD=max_completion_tokens
./course llm check
./course llm check --connect
```

### LM Studio

Load a chat model and start LM Studio's local server, then use its exact model
identifier. These settings assume its default port, 1234:

```sh
export BOOTCAMP_LLM_FEATURES=review,coach,handoff
export BOOTCAMP_LLM_BASE_URL=http://localhost:1234/v1
export BOOTCAMP_LLM_MODEL='<your-loaded-model-id>'
unset BOOTCAMP_LLM_API_KEY
export BOOTCAMP_LLM_TOKEN_FIELD=max_tokens
./course llm check
./course llm check --connect
```

If [LM Studio authentication](https://lmstudio.ai/docs/developer/core/authentication)
is enabled, set `BOOTCAMP_LLM_API_KEY` to its own token instead of leaving it
unset. An ambient `OPENAI_API_KEY` is never read automatically. Clear or replace
the bootcamp key whenever switching servers; changing the URL does not change
the credential. Do not place literal keys in command history or tracked files.

`check` is local configuration validation. `check --connect` explicitly sends
one small synthetic request, with no learner work, and requires an enabled
feature. Add `--json` for scripting. Run checks again after changing a model
or server. Clear `BOOTCAMP_LLM_FEATURES` to hide inference actions and prevent
new calls. A request already in flight can still finish; explicitly cancel
its pending ID if its result should be discarded.

## Learner actions

In guided delivery, `lr`, `lc`, and `lh` appear when the respective feature and
phase allow them. The terminal identifies the destination and model before
selection. Direct commands use the same saved-session implementation:

```sh
./course llm review --id my-session --phase c05.review
./course llm coach --id my-session --phase c02.calculate --family transfer
./course llm handoff --id my-session --role network-operations
./course llm handoff --id my-session --role network-operations --text 'Network operations owns the next check.'
```

Each command accepts `--json`. Headless clients can also use the existing
[session request envelope](README.md#start-a-session) with these actions:

| Action | Payload | When available |
| --- | --- | --- |
| `llm_review` | `{}` | Challenge 1–6 review, after the block's explanation and structural checks. |
| `llm_coach` | `family` | Conceptual checkpoint after a committed answer for that family. |
| `llm_handoff` | `role`; optional `text` | `c06.exchange`, after initial diagnosis, analysis, and written handoff. |
| `llm_cancel` | Pending `request_id` | Recovery, including when features are disabled. |

Review returns up to three findings with an exact quoted claim, evidence IDs,
explanation, and revision question. Coaching uses the recorded misconception
and asks one guiding question. Handoff roles are `network-operations`,
`architecture`, `security`, and `incident-response`; each unchanged handoff has
a maximum of three completed model turns. Reply to the previous question before
the next turn. The bound artifact regions and cited ledger rows define the
snapshot: changing them creates a different exchange. Changing only the role
does not reset the limit, and restoring an earlier snapshot reuses its history.

Start evaluation with Challenge 5. Review is also implemented for packet-path,
architecture, and capstone regions, but these features have not yet been
validated with learners. No LLM advice is available in the independent exit.

## Evidence, assessment, and privacy

Each feature sends a different selection of context:

| Feature | Learner content sent |
| --- | --- |
| Review | Current bound artifact regions, their cited ledger rows, the review guide, phase instructions, and opened evidence from that block. A prior explanation submission is required, but file edits since that submission are included. |
| Coaching | The latest committed checkpoint explanation for the selected family, its answers and deterministic feedback, question prompts, and opened evidence. It does not coach an assigned reassessment response or reread edited artifact prose. |
| Handoff | Current bound packet-path, architecture, and handoff regions, cited ledger rows, phase instructions, opened evidence, the selected role, and replies/questions from the same snapshot. |
| Authoring | A supported catalog example and its authored/computed facts; no learner session is read. |

Session evidence is limited to views opened in the same block at or before the
requested phase. Open every cited ledger record's evidence view before review
or handoff practice. Reading a file manually does not record a view action.

The client reuses saved command output. A partial case view remains partial;
it is never expanded to the complete source file. Incident-round records map
back to their original IDs. The context builder does not fetch future rounds,
reserved cases, unseen reassessment questions, linked worked solutions, or
unrelated files. It does not identify such material if a learner pastes it into
a selected field. Prompts treat quoted instructions as data, and the model has
no filesystem, browser, shell, or course-action tools. These restrictions do
not guarantee that generated advice is accurate or follows every instruction.

Feedback remains advisory: a valid citation does not prove that its conclusion
is correct. Only self/facilitator reviews supply rubric scores, and only the
existing Python checks establish factual correctness and completion.

Every delivered advice record counts as answer-bearing help. Coaching exposes
the current family; review and handoff advice expose their block. Previously
earned independent results remain intact. Unfinished exposed reassessments
remain practice, and fresh unassisted reassessment still uses the finite
authored catalog. Advice never modifies submissions or advances a phase.

Requests contain only the selected context, fixed task instructions, and model
settings. Hosted endpoints receive that content; their own data policies apply.
For loopback servers, requests bypass environment HTTP proxies. The client
adds the configured API key only to the authorization header. Redirects are
rejected, TLS is verified, and raw provider error bodies are not printed or saved.

Advisory history is stored locally under the session's ignored `work/` folder.
It records model, endpoint, prompt version, context hashes, evidence IDs,
latency, and token usage when available. Default JSON exports include LLM
metadata, status, and help history; default Markdown and phase CSV are shorter
summaries. Explicit `--include-artifacts` in JSON or Markdown adds private
advice and context. See the [export format table](README.md#export-commands).

## Failure and recovery

An accepted new inference request makes at most one provider call. Status,
cancellation, rejected requests, and replay make none. There is no automatic retry.
Context is limited to 64 KiB and response bodies to 256 KiB. Refusals,
truncation, malformed JSON, invalid quotes/citations, and connection failures
produce an unavailable advisory result rather than a wrong learner answer.
An operation can exit successfully while reporting `advisory_failed`. For
session actions, check `result.learning_result`; advice is present only for
`advisory_complete`. Exit code 0 means the operation was processed, not that
the model returned usable advice.

Advice that cannot be encoded as UTF-8, or contains the configured API key
after JSON decoding, is rejected before display or storage. This includes
JSON-escaped copies of that key. Valid accented text and emoji are preserved.
The credential check does not detect every possible secret in free text.

Requests reserve an ID before inference and release the session lock during
the call. Repeating a completed JSON request replays its saved result; a
duplicate in-flight request reports `advisory_pending` without another call.
Direct `./course llm review`, `coach`, and `handoff` commands allocate a new
request ID each time. To replay a lost response, retain and resubmit the same
`./course session act` request body; repeating a direct command requests new advice.
Advice is committed with its exposure record before it is returned. Edits or
other accepted actions during inference discard the stale result. Failed or
discarded advice does not change assessment eligibility.

Pending-request recovery remains available when LLM settings are absent or
invalid. Guided delivery shows the cancellation command and accepts ordinary
course actions without requiring a configured endpoint.

After interruption, inspect status and explicitly cancel a pending request:

```sh
./course session status --id my-session --json
./course llm cancel --id my-session --request-id PENDING_REQUEST_ID
```

Cancellation does not stop a request already accepted by the model server or
undo its possible usage charge. It prevents that result from being delivered.
Request new advice explicitly when ready. A lost response after a successful
commit preserves exposure and can be recovered by replaying the original
JSON request. Resuming the course never regenerates advice automatically.

Authentication failures usually mean a missing or mismatched endpoint token.
For incompatible-request errors, check the model and token-field setting. For
truncated results, increase the output budget or use another model. Missing
configuration, slow local inference, or unusable advice never blocks the
ordinary hints, rubric, or course progression.

Course/state/JSON protocol version 3 preserves older work with its matching
course copy. Do not migrate or regrade existing sessions silently. Endpoint,
key, and model changes do not invalidate a version-3 session.

## Maintainer drafting

Enable `author` explicitly and choose a new filename under `work/llm-drafts`:

```sh
export BOOTCAMP_LLM_FEATURES=author
./course llm author --family transfer --kind practice-variant --seed 7 --output transfer-draft.json
./course llm author --family timestamps --kind explanation --output time-explanation.json
```

Kinds are `explanation`, `sample-response`, and `practice-variant`. Drafts use
supported examples, never learner submissions or reserved reassessments. For
transfer practice candidates, Python chooses a seeded MTU outside the existing
catalog values and computes the answer. Other families use fixed supported
conditions for wording and distractor drafts. Relevant arithmetic is computed
locally; model output never becomes a trusted answer key automatically.

Draft files are private, marked unreviewed, and published atomically without
overwriting existing files. Check technical truth, independent answer keys,
equivalent difficulty, repeated conditions, and accidental answer cues before
promoting material. Follow normal catalog edits, versioning, and verification.
New session reassessments are never generated at runtime.

## Evaluation status and commands

No OpenAI or LM Studio model has been qualified in the current implementation
environment. Transport tests use simulated OpenAI and LM Studio responses,
including authenticated and unauthenticated settings. These tests establish
client behavior, not real-model quality or learning benefit.

Ten synthetic examples cover all four features, with calibration and held-out
splits. Their expectations are proposed checks, not facilitator annotations.
Run the offline inventory check without any LLM configuration:

```sh
python3 -B verification/check_llm.py --check
```

After configuring an endpoint and enabling the chosen feature, explicitly
collect model outputs for human review:

```sh
python3 -B verification/check_llm.py --live --feature review --split calibration --output review-calibration.json
python3 -B verification/check_llm.py --live --feature review --split held-out --output review-held-out.json
```

Repeat for `coach`, `handoff`, and `author`, and for each model/server setup.
Outputs go under `work/llm-evals`; use distinct names. Fill the facilitator
fields and record the actual server version. Schema-valid output is not a
quality pass. Compare grounding, useful revision questions, unsupported
criticism, uncertainty, answer leakage, latency, and usage. Use the
[pilot worksheet](../facilitator/pilot.md#optional-llm-comparison) for learner
trials and keep independent outcomes separate from supported revisions.
