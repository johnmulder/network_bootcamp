#!/usr/bin/env python3
"""Present and navigate the Network Bootcamp from one command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULES = tuple(sorted((ROOT / "modules").glob("module-*")))


def heading(path: Path, prefix: str = "# ") -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    try:
        display_path = path.relative_to(ROOT)
    except ValueError:
        display_path = path
    raise SystemExit(f"error: no {prefix.strip()} heading in {display_path}")


def numbered(items: tuple[Path, ...] | list[Path], number: int, label: str) -> Path:
    if not 1 <= number <= len(items):
        raise SystemExit(f"error: {label} must be between 1 and {len(items)}")
    return items[number - 1]


def sections(module: Path) -> tuple[Path, ...]:
    return tuple(sorted(module.glob("section-*")))


def guides(section: Path) -> tuple[Path, ...]:
    return tuple(sorted(section.glob("*.md")))


def quantity(count: int, noun: str) -> str:
    return f"{count} {noun if count == 1 else noun + 's'}"


def section_titles(module: Path) -> list[str]:
    titles = [
        line.split("—", 1)[1].strip()
        for line in (module / "README.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("## Section ") and "—" in line
    ]
    if len(titles) != len(sections(module)):
        raise SystemExit(f"error: section index mismatch in {module.relative_to(ROOT)}")
    return titles


def module_path(module_number: int) -> Path:
    return numbered(MODULES, module_number, "module")


def section_path(module_number: int, section_number: int) -> Path:
    return numbered(sections(module_path(module_number)), section_number, "section")


def guide_path(module_number: int, section_number: int, guide_number: int) -> Path:
    return numbered(
        guides(section_path(module_number, section_number)), guide_number, "guide"
    )


def workbench_path(module_number: int) -> Path:
    module = module_path(module_number)
    matches = tuple(module.glob("workbench/module*_workbench.py"))
    if len(matches) != 1:
        raise SystemExit(f"error: expected one workbench in {module.relative_to(ROOT)}")
    return matches[0]


def run_script(path: Path, *arguments: str) -> int:
    return subprocess.run(
        [sys.executable, "-B", str(path), *arguments],
        cwd=ROOT,
        check=False,
    ).returncode


def dashboard() -> int:
    print("Network Bootcamp")
    print("One Mac · saved evidence · open-source tools")
    print()
    for number, module in enumerate(MODULES, 1):
        module_sections = sections(module)
        guide_count = sum(len(guides(section)) for section in module_sections)
        print(
            f"{number}. {heading(module / 'README.md')} "
            f"({quantity(len(module_sections), 'section')}, "
            f"{quantity(guide_count, 'guide')})"
        )
    print()
    print("Start here")
    print("  Setup:     ./prerequisites/setup.sh")
    print("  Explore:   python3 course.py module 1")
    print("  Practice:  python3 course.py practice 1")
    print("  Verify:    python3 course.py verify")
    print()
    print("Write learner artifacts under work/. Saved evidence remains in labs/fixtures/.")
    return 0


def show_module(module_number: int) -> int:
    module = module_path(module_number)
    module_sections = sections(module)
    print(heading(module / "README.md"))
    print()
    for number, (section, title) in enumerate(
        zip(module_sections, section_titles(module)), 1
    ):
        print(f"{number}. {title} ({quantity(len(guides(section)), 'guide')})")
    print()
    print(f"Next: python3 course.py section {module_number} 1")
    return 0


def show_section(module_number: int, section_number: int) -> int:
    module = module_path(module_number)
    section = section_path(module_number, section_number)
    title = section_titles(module)[section_number - 1]
    print(f"{heading(module / 'README.md')} · Section {section_number}")
    print(title)
    print()
    for number, guide in enumerate(guides(section), 1):
        print(f"{number}. {heading(guide)}")
    print()
    print(f"Read: python3 course.py guide {module_number} {section_number} 1")
    return 0


def show_guide(module_number: int, section_number: int, guide_number: int) -> int:
    path = guide_path(module_number, section_number, guide_number)
    print(path.read_text(encoding="utf-8").rstrip())
    return 0


def practice(
    module_number: int,
    activity: str | None,
    demo: bool,
    seed: int,
    limit: int | None,
) -> int:
    script = workbench_path(module_number)
    if activity is None:
        return run_script(script, "list")
    if limit is not None and limit < 1:
        raise SystemExit("error: --limit must be at least 1")
    arguments = ["demo" if demo else "run", activity, "--seed", str(seed)]
    if limit is not None:
        arguments.extend(("--limit", str(limit)))
    return run_script(script, *arguments)


def timeline(source: str | None) -> int:
    arguments = ["timeline"]
    if source is not None:
        arguments.extend(("--source", source))
    return run_script(workbench_path(3), *arguments)


def verify() -> int:
    checks = (
        ("Evidence fixtures", ROOT / "labs" / "build_fixtures.py", ("--check",)),
        ("Module 1 workbench", workbench_path(1), ("self-test",)),
        ("Module 2 workbench", workbench_path(2), ("self-test",)),
        ("Module 3 workbench", workbench_path(3), ("self-test",)),
    )
    status = 0
    for label, script, arguments in checks:
        print(f"\n== {label} ==", flush=True)
        result = run_script(script, *arguments)
        if status == 0 and result != 0:
            status = result
    if status:
        print("\nCourse verification failed.", file=sys.stderr)
    else:
        print("\nCourse verification passed.")
    return status


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command")

    module = commands.add_parser("module", help="show one module's sections")
    module.add_argument("module", type=int)

    section = commands.add_parser("section", help="show one section's guides")
    section.add_argument("module", type=int)
    section.add_argument("section", type=int)

    guide = commands.add_parser("guide", help="print one guide")
    guide.add_argument("module", type=int)
    guide.add_argument("section", type=int)
    guide.add_argument("guide", type=int)

    practice_command = commands.add_parser(
        "practice", help="list or run a module's workbench activities"
    )
    practice_command.add_argument("module", type=int)
    practice_command.add_argument("activity", nargs="?")
    practice_command.add_argument("--demo", action="store_true")
    practice_command.add_argument("--seed", type=int, default=1)
    practice_command.add_argument("--limit", type=int)

    timeline_command = commands.add_parser(
        "timeline", help="show the normalized Module 3 incident timeline"
    )
    timeline_command.add_argument("--source")

    commands.add_parser("verify", help="verify fixtures and all workbenches")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command is None:
        return dashboard()
    if args.command == "module":
        return show_module(args.module)
    if args.command == "section":
        return show_section(args.module, args.section)
    if args.command == "guide":
        return show_guide(args.module, args.section, args.guide)
    if args.command == "practice":
        return practice(args.module, args.activity, args.demo, args.seed, args.limit)
    if args.command == "timeline":
        return timeline(args.source)
    return verify()


if __name__ == "__main__":
    sys.exit(main())
