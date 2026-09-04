# Interactive Course Plan

## Goal

Make the first course experience feel guided while preserving every existing
command and keeping the project dependency-free.

Status: implemented and verified.

## Iteration 1 — Natural Entry

- [x] Add `./course` as the memorable root command.
- [x] Keep `python3 course.py ...` working for existing documentation and
  scripts.
- [x] Make setup finish by pointing learners to `./course`.

Success: `./course module 1` works from any directory.

## Iteration 2 — Guided Navigation

- [x] Show a numbered home menu when `./course` is run in a terminal.
- [x] Let learners choose modules, sections, and guides without learning command
  syntax.
- [x] Page long guides and show a breadcrumb before the content.
- [x] Keep the concise dashboard when output is redirected or scripted.

Success: a learner can reach the first guide using only Enter and number keys.

## Iteration 3 — Friendlier Practice

- [x] Add a numbered five-question practice menu for each module.
- [x] Let learners ask for input help or reveal an answer explicitly.
- [x] Give one retry before revealing a missed answer.
- [x] Preserve seeded `run` and `demo` commands for repeatable facilitation.

Success: guided practice works without knowing activity names, while existing
workbench commands remain compatible.

## Iteration 4 — Verification and Handoff

- [x] Cover the launcher, guided navigation, practice menus, help, retry, and
  non-interactive compatibility with automated tests.
- [x] Run fixture verification, all tests, Markdown lint, and Git whitespace
  checks.
- [x] Commit only after every check passes.

## Deliberate Boundary

Do not add a web application, third-party terminal UI, accounts, or persistent
progress tracking. Add progress state only when learners need cross-session
resume behavior that the existing `work/` artifacts cannot provide.
