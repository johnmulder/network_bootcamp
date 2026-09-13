# Network Bootcamp

A six-hour networking bootcamp built around six practical challenges: follow
a packet, diagnose a stalled transfer, handle a routing failure, defend a
design, investigate suspicious activity, and brief the next shift.

The course runs on one Mac laptop. Its core exercises use local, saved evidence
and open-source tools; no virtual machines, containers, cloud accounts,
enterprise hardware, or proprietary analyzers are required.

## Current State

| Curriculum element | Implemented material |
| --- | --- |
| Course / session protocol / learning contract | 3.0 / 3 / 2 |
| Required one-day challenges | 6, plus opening and individual exit |
| Required learner deliverables | 3 connected bundles |
| Modules in the reference library | 3 |
| Sections | 23 |
| Detailed subsection guides | 104 |
| Interactive workbenches | 3 |
| Workbench questions | 83 |
| Saved delivery | 36 phases, with terminal and JSON interfaces |
| Evidence fixtures | 36 manifest-tracked files plus the manifest |
| Incident timeline | 17 normalized events across 8 sources |
| Automated tests | Standard-library tests plus complete delivery rehearsals |
| Optional LLM support | Review, coaching, handoff practice, and maintainer drafts |
| Supported environment | One Mac laptop with local, open-source tools |

The [course agenda](agenda.md) is the authoritative curriculum specification.
This README is the operational entry point for using the implemented material.

Six teaching hours plus 60 minutes of breaks is the planned schedule, with
installation additional. The [validation record](facilitator/validation.md)
reports software and model-specific checks separately from learner trials.
Observed learner attainment, class duration, and the learning benefit of LLM
feedback have not been established.

## Start Here

Follow the [one-day challenge path](challenges/README.md) for six teaching
hours, with breaks and lunch additional. Its short briefs, pocket reference,
hints, and shared templates replace separate submissions for every guide.
Facilitators use the [teaching guide](facilitator/README.md), solutions, and
pilot worksheet. The [module library](modules/README.md) remains available for
extended study.

From the repository root, install the course tools and verify the saved
evidence fixtures:

```bash
./prerequisites/setup.sh
```

Open the guided course:

```bash
./course
```

Confirm that the installed tools and course evidence are ready:

```bash
./prerequisites/setup.sh --check
./course verify
```

The setup process and each command are explained in the
[prerequisites guide](prerequisites/README.md). Begin the required curriculum with
[Start the Shift](challenges/README.md#start-the-shift--15-minutes).

## Course Navigator

`./course` opens a numbered menu when run in a terminal. Press Enter to start
or resume the six-hour course. The runner presents one phase at a time, offers
named evidence views and hints, and saves accepted responses. Quit with q and
return later. Edit the three deliverables in the displayed session directory.
The menu also offers the reference library, optional practice, full timeline,
verification, and read-only challenge browsing.

The menu uses the session ID `bootcamp`, stored under `work/bootcamp/`. Use
`./course learn --id my-session` for another workspace, including when
`work/bootcamp/` already contains manually created files. Without a terminal,
`./course` prints a command index; saved automation uses `./course session`.

Direct commands remain available for repeatable facilitation and scripting:

| Goal | Command |
| --- | --- |
| Open the guided course | `./course` |
| Start or resume a named session | `./course learn --id my-session` |
| Check core tool capabilities | `./course doctor --json` |
| Inspect a saved session from a script | `./course session status --id my-session --json` |
| Read the one-day schedule and start instructions | `./course day` |
| Read a challenge | `./course challenge 1` |
| List a module's sections | `./course module 1` |
| List a section's guides | `./course section 1 2` |
| Read a guide | `./course guide 1 2 3` |
| List a module's practice activities | `./course practice 1` |
| Preview a short worked activity | `./course practice 1 routes --demo --limit 4` |
| Start scored practice | `./course practice 2 cloud --seed 7` |
| Show the incident timeline | `./course timeline` |
| Filter the timeline to one source | `./course timeline --source endpoint` |
| Verify fixtures and all workbenches | `./course verify` |

Reference navigation reads the existing directory hierarchy and Markdown.
Guided delivery uses [36 defined phases](delivery/course.json), with content
fragments in those same documents. Progress and learner responses are stored
locally under `work/<session-id>/`, which Git ignores. Core delivery sends no
learner data. Optional LLM actions send selected context to a configured server.
`python3 course.py ...` remains a supported equivalent for automation. See the
[delivery guide](delivery/README.md) for JSON requests, version matching,
reviews, and recovery. A successful command is not a passing assessment.
The [completion policy](agenda.md#completion-and-feedback) distinguishes
finished delivery, passing rubric reviews, and independent completion.

## Optional LLM Support

[LLM support](delivery/llm.md) is disabled by default and independently enables
review, coaching, handoff practice, or maintainer drafting. Configure a base
URL and model to use OpenAI or local LM Studio. Supply an endpoint-specific
API key when the server requires authentication; an unauthenticated local
server needs no key.
The guide includes both setup examples and the optional connection check.
The complete course remains usable offline with no credentials or model server.

Advice is recorded as help and does not award scores or replace human reviews.
Real-model qualification and learner trials remain pending; the implementation
includes synthetic evaluation cases and an explicit evaluation command.

## Reference Library

| Module | Material | Interactive support | Primary learner artifact |
| --- | --- | --- | --- |
| [1 — Operational Networking](modules/module-01-operational-networking/README.md) | 8 sections, 43 guides | [6 activities and 25 questions](modules/module-01-operational-networking/workbench/README.md) | Evidence-backed packet-path review |
| [2 — Network Architecture](modules/module-02-network-architecture/README.md) | 8 sections, 29 guides | [5 activities and 30 questions](modules/module-02-network-architecture/workbench/README.md) | Annotated architecture and failure assessment |
| [3 — Incident Response and Integration](modules/module-03-incident-response-and-integration/README.md) | 7 sections, 32 guides | [5 activities and 28 questions](modules/module-03-incident-response-and-integration/workbench/README.md) | Evidence ledger, incident narrative, and cross-functional handoff |

The modules form one progression:

1. Trace forwarding decisions and validate them with network evidence.
2. Evaluate how components, boundaries, and failure domains affect a path.
3. Correlate telemetry, qualify claims, and communicate an incident assessment.

The [module index](modules/README.md) describes the repeatable workflow for
combining each guide, its saved evidence, and the interactive workbench.

## Repository Map

```text
.
├── README.md          # Operational entry point
├── agenda.md          # Authoritative curriculum and completion standards
├── course             # Natural guided-course command
├── course.py          # Short course navigation and practice commands
├── delivery.py        # Saved sessions, evidence actions, and assessment state
├── learning.py        # Deterministic scoring, reassessment, and experiments
├── llm.py             # Optional HTTP client, validation, and maintainer drafts
├── llm_delivery.py    # Session context, advisory history, and help exposure
├── delivery/          # Course definition and automation contract
├── prerequisites/    # Mac setup, tool roles, and readiness checks
├── labs/             # Fixture builder and reproducible saved evidence
├── challenges/       # One-day briefs, reference card, hints, and templates
├── facilitator/      # Teaching notes, solutions, and pilot worksheet
├── modules/          # Reference guides, section directories, and workbenches
├── tests/            # Standard-library project test suite
└── verification/     # Content checks, delivery rehearsals, and course packaging
```

Learner-created diagrams, notes, command output, ledgers, and assessments go
under `work/`. That directory is created while working through the exercises
and is intentionally separate from the generated fixtures in `labs/fixtures/`.

## Evidence and Safety Model

The core course is deterministic: it reads versioned packet captures, route
tables, architecture records, and incident telemetry from
[`labs/fixtures/`](labs/fixtures/). This path does not require elevated
privileges and does not contact external systems.

Some guides also show optional live observations with macOS networking tools.
Only packet capture requires `sudo`; capture only traffic on the learner's own
Mac or on a network where capture is explicitly authorized. The saved fixtures
remain the reference evidence when live capture is unavailable or inappropriate.

## Automated Tests

Run the complete project test suite from the repository root:

```bash
python3 -B -m unittest discover -s tests -v
```

The suite exercises the course navigator, fixture builder, all three
workbenches, setup, saved delivery, and optional LLM support. It covers packet
construction, routing and architecture decisions, timeline correlation,
question identity,
staged evidence, save/resume, concurrent requests, failure recovery, artifact
validation, review staleness, reassessment, and private exports. LLM tests use
mocked HTTP responses to check configuration, output validation, credential
handling, interrupted requests, and assessment exposure; they do not qualify
a real provider or model.

Tests build fixtures only in temporary directories. Setup tests use simulated
macOS and Homebrew commands, so they never install software or depend on the
host's current package state. Python's `-B` option prevents bytecode cache files
from being written into the course tree.

With the core Mac tools available, rehearse both case assignments through all
36 phases using fresh processes and synthetic learner responses:

```sh
python3 -B verification/check_delivery.py --smoke --journey
```

See the [delivery guide](delivery/README.md#verify-and-package-delivery) for
portable content checks, CI, and building a course archive. The
[validation record](facilitator/validation.md) distinguishes technical checks
from the learner pilot that remains to be conducted.

## Documentation Guide

- [One-day route](challenges/README.md): timed challenges and shared outputs.
- [Facilitator guide](facilitator/README.md): reveal points, rubric, and delivery.

- [Agenda](agenda.md): course intent, module content, exercises, and completion
  standards.
- [Prerequisites](prerequisites/README.md): supported environment, installation,
  tool roles, and validation.
- [Lab fixtures](labs/README.md): evidence inventory, regeneration, checksums,
  and workbench relationships.
- [Module index](modules/README.md): curriculum navigation and learning routine.
- Module READMEs: section-by-section reading order and the relevant workbench.
- Section guides: evidence exercises with commands and completion checks,
  plus the explicitly conceptual VXLAN/EVPN reference.

## Maintainer Validation

Course participants do not need a Markdown linter. Maintainers who have
`markdownlint-cli2` installed can validate all documentation with:

```bash
markdownlint-cli2 "**/*.md"
git diff --check
```
