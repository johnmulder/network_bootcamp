#!/usr/bin/env python3
"""Build a local course archive from tracked files and test the extracted copy."""

from __future__ import annotations

import argparse
import gzip
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import delivery as d


def package(output: Path) -> None:
    d.definition()
    d.evidence_integrity()
    exemplars = d.module_at("labs/exemplars/manage.py")
    exemplars.verify()
    result = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"], check=True, capture_output=True)
    names = sorted(name for name in result.stdout.decode().split("\0") if name
                   and name != "PLAN.md" and not any(part in {"work", ".git", "__pycache__"} for part in Path(name).parts))
    metadata = dict(format_version=1, **d.versions(d.definition()),
                    exemplars_sha256=exemplars.fingerprint())
    members = [(name, d.confined(ROOT, name)) for name in names]
    for name, path in members:
        if not path.is_file() or path.is_symlink():
            raise d.DeliveryError(f"Archive requires a regular tracked file: {name}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for name, path in members:
                    content = path.read_bytes()
                    info = tarfile.TarInfo("network_bootcamp/" + name)
                    info.size = len(content)
                    info.mode = path.stat().st_mode & 0o777
                    archive.addfile(info, io.BytesIO(content))
                content = (json.dumps(metadata, indent=2) + "\n").encode()
                info = tarfile.TarInfo("network_bootcamp/RELEASE.json")
                info.size, info.mode = len(content), 0o644
                archive.addfile(info, io.BytesIO(content))
    print(f"Built {output}: {len(names)} tracked files plus RELEASE.json", flush=True)


def check_archive(output: Path, journey: bool = False) -> None:
    with tempfile.TemporaryDirectory(prefix="bootcamp package ") as temp:
        base = Path(temp)
        with tarfile.open(output, "r:gz") as archive:
            # Only extract our regular members; avoid version-specific tar filters.
            for member in archive.getmembers():
                if not member.isfile() or any(part in {"work", ".git"} for part in Path(member.name).parts):
                    raise d.DeliveryError("Unexpected member in course archive")
                path = d.confined(base, member.name)
                path.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as source, path.open("xb") as target:
                    target.write(source.read())
                path.chmod(member.mode & 0o777)
        root = base / "network_bootcamp"
        if (root / ".git").exists() or (root / "work").exists() or (root / "PLAN.md").exists():
            raise d.DeliveryError("Archive contains development or learner data")
        commands = [[str(root / "course"), "verify"],
                    [sys.executable, "-B", str(root / "verification/render_diagrams.py")],
                    [sys.executable, "-B", str(root / "verification/check_curriculum.py")],
                    [str(root / "course"), "llm", "check", "--json"],
                    [sys.executable, "-B", str(root / "verification/check_llm.py"), "--check"],
                    [sys.executable, "-B", str(root / "verification/check_delivery.py")]]
        if journey:
            commands += [[str(root / "course"), "doctor", "--json"],
                         [sys.executable, "-B", str(root / "labs/exemplars/manage.py"), "--decode"],
                         [sys.executable, "-B", str(root / "verification/check_curriculum.py"), "--smoke"],
                         [sys.executable, "-B", str(root / "verification/check_delivery.py"), "--smoke", "--journey"]]
        environment = {key: value for key, value in os.environ.items()
                       if not key.startswith("BOOTCAMP_LLM_") and key != "OPENAI_API_KEY"}
        for command in commands:
            subprocess.run(command, cwd=base, check=True, env=environment)
        metadata = json.loads((root / "RELEASE.json").read_text())
        code = "import json, delivery; print(json.dumps(delivery.versions(delivery.definition())))"
        result = subprocess.run([sys.executable, "-B", "-c", code], cwd=root, check=True, capture_output=True, text=True)
        if any(metadata[key] != value for key, value in json.loads(result.stdout).items()):
            raise d.DeliveryError("Packaged content does not match release metadata")
        code = "import delivery; print(delivery.module_at('labs/exemplars/manage.py').fingerprint())"
        result = subprocess.run([sys.executable, "-B", "-c", code], cwd=root, check=True, capture_output=True, text=True)
        if metadata["exemplars_sha256"] != result.stdout.strip():
            raise d.DeliveryError("Packaged exemplars do not match release metadata")
        print("Extracted archive passed verification at a path containing spaces, without Git metadata.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new .tar.gz path; never overwrites")
    parser.add_argument("--check", action="store_true", help="extract and verify the package")
    parser.add_argument("--journey", action="store_true", help="also run real-tool doctor, smoke, and both course journeys")
    args = parser.parse_args()
    try:
        package(args.output)
        if args.check or args.journey:
            check_archive(args.output, args.journey)
        return 0
    except (d.DeliveryError, OSError, subprocess.SubprocessError, ValueError) as error:
        print(f"Packaging failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
