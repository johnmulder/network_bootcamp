# Network Bootcamp

A practical networking course for learning how packets move, how network
architecture shapes that movement, and how to use network evidence during an
incident investigation.

The course runs on one Mac laptop. Its core exercises use local, saved evidence
and open-source tools; no virtual machines, containers, cloud accounts,
enterprise hardware, or proprietary analyzers are required.

## Current State

| Curriculum element | Implemented material |
| --- | --- |
| Modules | 3 |
| Sections | 23 |
| Detailed subsection guides | 104 |
| Interactive workbenches | 3 |
| Workbench questions | 79 |
| Evidence fixtures | 36 manifest-tracked files plus the manifest |
| Incident timeline | 17 normalized events across 8 sources |
| Automated tests | 33 tests across all 7 executable sources |
| Supported environment | One Mac laptop with local, open-source tools |

The [course agenda](agenda.md) is the authoritative curriculum specification.
This README is the operational entry point for using the implemented material.

## Start Here

From the repository root, install the course tools and generate the local
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
[prerequisites guide](prerequisites/README.md). Begin the curriculum with
[Module 1](modules/module-01-operational-networking/README.md).

## Course Navigator

`./course` opens a numbered menu when run in a terminal. Press Enter to follow
the recommended path through Module 1, or choose a module, short practice
session, incident timeline, or verification. Long guides use the terminal
pager, so they can be read without losing your place.

Direct commands remain available for repeatable facilitation and scripting:

| Goal | Command |
| --- | --- |
| Open the guided course | `./course` |
| List a module's sections | `./course module 1` |
| List a section's guides | `./course section 1 2` |
| Read a guide | `./course guide 1 2 3` |
| List a module's practice activities | `./course practice 1` |
| Preview a short worked activity | `./course practice 1 routes --demo --limit 4` |
| Start scored practice | `./course practice 2 cloud --seed 7` |
| Show the incident timeline | `./course timeline` |
| Filter the timeline to one source | `./course timeline --source endpoint` |
| Verify fixtures and all workbenches | `./course verify` |

The navigator calculates the hierarchy from the module directories and reads
titles and content from the checked-in Markdown. It does not track progress or
write learner data. `python3 course.py ...` remains a supported equivalent for
automation.

## Learning Path

| Module | Material | Interactive support | Primary learner artifact |
| --- | --- | --- | --- |
| [1 — Operational Networking](modules/module-01-operational-networking/README.md) | 8 sections, 43 guides | [5 activities and 21 questions](modules/module-01-operational-networking/workbench/README.md) | Evidence-backed packet-path review |
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
├── PLAN.md            # Interactive course implementation plan
├── agenda.md          # Authoritative curriculum and completion standards
├── course             # Natural guided-course command
├── course.py          # Short course navigation and practice commands
├── prerequisites/    # Mac setup, tool roles, and readiness checks
├── labs/             # Fixture builder and reproducible saved evidence
├── modules/          # Guides, section directories, and workbenches
└── tests/            # Standard-library project test suite
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
workbenches, and the setup script. It covers navigation, command delegation,
protocol construction, fixture generation and corruption, routing decisions,
architecture decisions, incident timeline correlation, question and CLI
behavior, and setup success and failure paths.

Tests build fixtures only in temporary directories. Setup tests use simulated
macOS and Homebrew commands, so they never install software or depend on the
host's current package state. Python's `-B` option prevents bytecode cache files
from being written into the course tree.

## Documentation Guide

- [Agenda](agenda.md): course intent, module content, exercises, and completion
  standards.
- [Prerequisites](prerequisites/README.md): supported environment, installation,
  tool roles, and validation.
- [Lab fixtures](labs/README.md): evidence inventory, regeneration, checksums,
  and workbench relationships.
- [Module index](modules/README.md): curriculum navigation and learning routine.
- Module READMEs: section-by-section reading order and the relevant workbench.
- Section guides: exact teaching instructions, evidence commands, expected
  observations, questions, and completion checks.

## Maintainer Validation

Course participants do not need a Markdown linter. Maintainers who have
`markdownlint-cli2` installed can validate all documentation with:

```bash
markdownlint-cli2 "**/*.md"
git diff --check
```
