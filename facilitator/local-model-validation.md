# Local Model Evaluation — September 13, 2026

This record concerns the user's running local model and synthetic course
examples. It does not establish compatibility with smaller models, general
reliability, or learner benefit. Quality judgments below are agent judgments;
facilitator annotations and learner trials remain outstanding.

## Observed Configuration

| Setting | Value |
| --- | --- |
| Server | LM Studio 0.4.24+1 |
| Model | `openai/gpt-oss-120b` |
| Format and quantization | GGUF, MXFP4, 4 bits per weight |
| Hardware | Apple M3 Max, 128 GiB RAM |
| Loaded context | 44,032 tokens, reported by `/api/v1/models` |
| Course API root | `http://localhost:1234/v1` |
| Authentication | Disabled for these local requests |
| Input budget | 16,384 bytes including serialized messages and schema |
| Output allowance | 2,048 tokens using `max_tokens` |
| Network timeout | 180 seconds per blocking operation |
| Initial latency target | At most 60 seconds per observed request |
| Sampling | Existing server defaults; unchanged and not independently measured |

The user's native `/api/v1/chat` example identified the server and loaded
model. The course used that same server's `/v1/chat/completions` endpoint.
Both prompt-only and schema-mode connection probes succeeded. No native-API
adapter or hosted fallback was needed. The model was already loaded; these
are warm-model measurements, not cold-start or controlled memory benchmarks.

## Method and Calibration

The ten existing synthetic cases were frozen before inference: five
calibration and five held-out examples across review, coaching, handoff, and
authoring. Each selected split was repeated three times. The initial budget
was 80 provider calls across probes, calibration, and session tests.

Prompt version 2 produced 12/15 locally valid calibration responses in each
mode. All three coaching responses failed in each mode. Schema-mode rejected
outputs cited `conditions`, which was outside the supplied evidence object.
Reviews also sometimes failed to challenge definite unsupported claims or
requested revisions to already qualified conclusions.

These calibration observations led to prompt version 3: schema-mode citations
are constrained to actual evidence IDs, with an empty array when none exist,
and review instructions distinguish unsupported claims from correct qualified
claims. Local validation was retained. The revised schema profile passed local
validation on all 15 calibration responses. It still produced a false-positive
review, wording that conflated successful authentication with legitimacy,
and incorrect TCP-options descriptions in drafts. One draft took 69.6 seconds,
exceeding the initial target. Transport success therefore did not qualify
review or authoring quality.

Only the selected schema profile proceeds to held-out testing after these
calibration changes. Prompt-only mode remains unqualified. This adjustment
preserves untouched held-out cases and stays within the overall call budget.
The version-3 configuration is frozen before inspecting held-out responses.

## Results

The run made **68 provider calls**, within the 80-call budget. Of those, 60
returned advice accepted by local validation. There were no automatic retries,
connection failures, context overflows, or truncated responses. Eight rejected
responses were advice-validation failures: six during initial coaching
calibration and two during held-out review.

| Run | Locally valid / calls |
| --- | ---: |
| Version 2 connection probes, both modes | 2/2 |
| Version 2 prompt-mode calibration | 12/15 |
| Version 2 schema-mode calibration | 12/15 |
| Version 3 schema-mode calibration | 15/15 |
| Version 3 schema-mode held-out examples | 13/15 |
| Version 3 saved-session rehearsal | 6/6 |

Version-3 results below combine calibration, held-out cases, and the saved
session rehearsal. Timing includes failed requests. These are observed
end-to-end timings during a development session, not controlled benchmarks.

| Feature | Locally valid / calls | Median / maximum seconds | Decision |
| --- | ---: | ---: | --- |
| Coaching | 7/7 | 6.51 / 28.27 | Provisional starting feature for the tested transfer explanations; no replacement answers identified. |
| Handoff | 9/9 | 3.87 / 12.48 | Provisional starting feature for the tested roles/case; the three-turn exchange repeated a similar question. |
| Review | 12/14 | 11.35 / 26.68 | Unqualified: false-positive calibration review, uncertainty overstatement, and held-out citation failures. |
| Authoring | 6/6 | 25.20 / 69.64 | Unqualified: correct main arithmetic but incorrect technical wording/distractor explanations; one request exceeded the latency target. |

Held-out review correctly challenged the unsupported execution/exfiltration
claim in all three repetitions. In the injection case, one accepted response
quoted the synthetic attack marker while declining the request, contrary to
the proposed expectation. Two responses lacked the required finding citations
and were discarded. No reserved-case data was revealed. Prompts and settings
were not changed after inspecting held-out results.

All three held-out drafts retained the supplied 1,288-byte bound and fit
answer, but their distractor explanations contained errors. For example,
omitting TCP overhead was described as reducing the available payload rather
than increasing it. These drafts need technical editing before publication.

The saved-session rehearsal used real evidence commands, actual context
construction, and temporary synthetic artifacts. Coaching, incident review,
three handoff turns, and capstone review completed. Both reviews returned no
findings and insufficient evidence for the synthetic structural prose; that
does not establish useful rubric-review quality. Replay made no additional
calls, default exports omitted private text, explicit private exports retained
advice, and an over-budget request was rejected without changing the session
or contacting the server.

The largest observed input was 13,918 bytes. Successful requests reported at
most 3,394 prompt tokens and 653 completion tokens. These observed maxima are
not sizing guarantees for other submissions. A single mid-run system sample
showed no swap or compressed pages; peak memory was not measured.

Coaching coverage was the transfer family; standalone handoff roles were
network operations and security, with a case-A network-operations exchange.
Other families, roles, cases, smaller models, and learner outcomes remain
unqualified. The suggested starting profile enables only coaching and handoff
and retains the normal hints, rubric, and human judgment.

## Context and Reproducibility

The initial real-context snapshots measured 16,014 bytes for incident review
and 5,610 bytes for a handoff. Compact context measured 10,247 and 3,721 bytes
respectively, before fixed prompt/schema overhead. All evidence IDs were
retained. The saved original context remains available for validation and
artifact hashing. These are synthetic examples, not maximum-size guarantees.

The [LLM guide](../delivery/llm.md) documents configuration and evaluation
commands. Raw synthetic outputs, the request log, protocol, and agent review
are kept under ignored `work/llm-evals/`; no credentials or learner records
are included in this report. Ordinary tests and verification never contact
a model server. No OpenAI-hosted endpoint was tested in this run.

The evaluated inference code is commit `283352c`, prompt version 3. The final
offline suite passed all 110 tests, including 35 focused LLM tests. Course
verification, all 31 real-tool views, both full A/B and B/A journeys, Python
3.10 syntax checks for 17 sources, Markdown lint, local links, and Git
whitespace checks passed. These checks do not qualify generated prose.
