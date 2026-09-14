# Expanded Local Model Evaluation — September 13, 2026

This second round evaluates the user's running local model against broader
synthetic learner work. It preserves the [first report](local-model-validation.md)
as history. Content judgments are by Codex; facilitator review and actual
learner trials remain pending. The results do not qualify smaller models or
OpenAI-hosted endpoints.

## Setup and Method

The server remained LM Studio 0.4.24+1 at `http://localhost:1234/v1`, running
`openai/gpt-oss-120b` as GGUF MXFP4 on an Apple M3 Max with 128 GiB RAM and
44,032 loaded context tokens. Authentication was disabled. The run used schema
mode, `max_tokens`, 2,048 output tokens, a 16,384-byte input allowance, and a
180-second timeout per blocking operation. Sampling defaults were unchanged
and not independently measured. These are warm-model development-session
timings, not controlled performance or peak-memory benchmarks.

The new inventory contains 32 calibration and 80 held-out cases: all 11
coaching families, six review phases, four recipient roles, both capstone
cases, and transfer authoring. Coaching maps to 22 objectives; the three
independent-exit objectives remain excluded. Fresh coaching conditions derive
from supported examples rather than the reserved reassessment bank. The old
ten cases are historical regressions, not fresh held-out evidence.

Cases, expectations, settings, prompts, and call limits were recorded before
use. Before candidate tuning or held-out inference, two capstone review cases
received an omitted supporting state view. The previous inventory hash and
correction are retained. A mistyped probe revision label was also corrected
in the audit record without changing its request or outcome.

## Calibration Decisions

Prompt version 3 produced valid output on all 32 baseline cases, but coaching
usually described internal feedback codes. Review falsely criticized a valid
unknown-authorization claim. A draft's distractor numbers did not match their
stated arithmetic operations.

Version 4 removed coaching jargon and handled that specific review case better,
but introduced a wrong routing assertion and supplied replacement answers in
several coaching examples. That coaching wording was rejected. Version 5 used
the 16-call diagnostic reserve to test more conservative instructions. Its UTC
paraphrase exposed a remaining problem: model wording could change an already
trusted explanation.

The final implementation, prompt version 6 at commit `ab3b324`, preserves the
course's deterministic coaching feedback verbatim and uses the model for the
guiding question. It retains local citation and output validation. Handoff,
review, and drafting limitations were recorded before freezing version 6 for
held-out testing; there was no subsequent prompt tuning on held-out results.
Later edits clarify terminal navigation and documentation without changing
the evaluated inference behavior.

## Results

The round recorded **190 attempts**, within the 200-attempt limit. One connection
attempt failed inside the sandbox. The explicitly authorized confirmation
succeeded. Of 189 attempts that produced provider responses, 188 were accepted
by local output validation; one incident-review response was discarded as
invalid advice. There were no automatic retries or unresolved pending attempts.
The accepted total includes one readiness probe.

| Stage | Accepted / attempts |
| --- | ---: |
| Connection probes | 1/2 |
| Version 3 baseline | 32/32 |
| Version 4 candidate | 32/32 |
| Version 5 diagnostics | 16/16 |
| Version 6 held-out | 80/80 |
| Version 6 sessions, repeats, and explicit replies | 27/28 |

The final-version table combines held-out cases with saved-session rehearsals,
eight additional samples of four previously observed inputs, and two explicit
learner-correction checks. These calls are not all independent examples. Failed
responses are included in timing summaries.

| Feature | Accepted / calls | Median / maximum seconds |
| --- | ---: | ---: |
| Coach | 41/41 | 3.19 / 6.60 |
| Handoff | 36/36 | 6.23 / 32.10 |
| Review | 21/22 | 8.32 / 15.93 |
| Author | 9/9 | 14.97 / 18.54 |

No observed request exceeded the 60-second target. The largest input was
15,621 bytes. Accepted responses reported at most 3,673 prompt tokens and 701
completion tokens. These maxima do not establish safe sizing for other work
or models. The 2,048-token allowance was retained; no smaller-budget comparison
was needed to address observed latency.

### Content Findings

- Coaching: all 33 held-out questions were inspected. No explicit replacement
  factual answer was identified in those questions. The explanation now matches
  the recorded deterministic feedback by construction. Some questions still
  repeat reasoning or are awkward, such as asking how to verify enforcement
  without telemetry. This is the preferred starting feature for this tested
  setup, with questions treated as advisory.
- Review: all six deliberately mistaken claims received findings, but three
  of six correctly qualified claims also received findings. The model confused
  “not established” with “definitely did not happen.” The targeted qualified
  authentication case remained sound across its held-out response and two
  repeats; that success did not generalize to other uncertainty statements.
  Review remains experimental and is not recommended for unsupervised use.
- Handoff: all eight three-turn held-out exchanges returned valid responses.
  Case-A exchanges repeatedly asked for change records; case-B exchanges often
  pursued a firewall-deny premise despite the earlier no-route observation and
  supplied permitting conditions. Real-session questions sometimes alleged
  that provided snapshots were missing or confused the client subnet with the
  external destination. One explicit learner correction improved the next
  question; another was misrepresented. Handoff remains experimental, replacing
  the first report's provisional recommendation for this local setup.
- Authoring: all seven held-out drafts retained the primary calculated bound
  and fit answer. Explanations still confused omitted TCP-header bytes with
  option bytes, or confused payload size with packet size. A repeat of a
  previously sound drafting input produced erroneous fit reasoning. Drafts
  require technical editing and independent maintainer review before use.

Valid output is therefore a transport and contract result, not a quality pass.
No feature received facilitator approval or demonstrated a learner outcome.

## Learner Experience and Limits

The terminal presents advice as readable text, shows prerequisites and waiting
messages, displays the preceding handoff question and remaining turns, and
provides local-only saved-advice access. History identifies advice for earlier
work. Errors direct learners back to existing course support. JSON automation,
first attempts, help exposure, independent exits, and private exports retain
their existing boundaries.

The expanded session rehearsals use meaningful but intentionally partial
artifacts, real evidence commands, corrected answers, UTC feedback, and revised
handoffs. They are not high-scoring learner exemplars. Scripted handoff replies
use the preceding question and distinguish attempted adequate, incomplete,
and incorrect responses. A scripted reply labeled adequate may still omit a
specific detail requested by the model; repetition must be judged against the
actual reply. No learning benefit is inferred from these rehearsals.

## Reproducibility

The frozen run and incremental attempt records are under ignored
`work/llm-evals/round2/`; raw synthetic session records, the freeze decision,
and agent review are alongside it. Attempts are committed before sending,
including failures and interruptions. Explicit replay makes no new call.
Credentials and real learner records are not included. The
[LLM guide](../delivery/llm.md#evaluation-status-and-commands) describes the
reusable evaluation commands.

## Software Validation

All 118 standard-library tests passed, including 43 focused LLM tests. Course
verification passed for 36 fixtures, 83 questions, 36 phases, and the 17-event
timeline. All 31 real-tool views and both complete A/B and B/A journeys passed.
The extended session rehearsals checked default-export privacy, explicit
private history, rereading advice without changes, request replay, and input
budget rejection before inference. Reconstructing both rehearsals from saved
results made no additional model calls.

All features remain disabled by default. No hosted endpoint was contacted,
no drafts were promoted, and no learner scores were assigned by the model.
Existing sessions require their matching course copy when the assessed-content
fingerprint changes; no sessions were silently migrated or regraded.
