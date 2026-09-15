#!/usr/bin/env python3
"""Check reference coverage and optionally execute the documented read-only views."""

import argparse
from pathlib import Path
import re
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def check(smoke=False):
    guides = sorted((ROOT / 'modules').glob('module-*/section-*/*.md'))
    matrix = (ROOT / 'modules/evidence-matrix.md').read_text()
    errors, commands = [], set()
    if len(guides) != 104:
        errors.append(f'Expected 104 guides, found {len(guides)}')
    for path in guides:
        text = path.read_text()
        relative = str(path.relative_to(ROOT / 'modules'))
        if matrix.count(f']({relative})') != 1:
            errors.append(f'Matrix needs one row for {relative}')
        for section in ('## Core Model', '## Teaching Instructions',
                        '## Expected Evidence and Worked Reasoning',
                        '## Completion Standard', '## Sources'):
            if text.count(section) != 1:
                errors.append(f'{relative}: missing or repeated {section}')
        for block in re.findall(r'```sh\n(.*?)\n```', text, re.S):
            commands.update(line for line in block.splitlines() if line.strip())
    if smoke:
        for command in sorted(commands):
            result = subprocess.run(shlex.split(command), cwd=ROOT, capture_output=True,
                                    text=True, timeout=30)
            if result.returncode:
                errors.append(f'{command}: {result.stderr.strip()}')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'Reference checks passed: {len(guides)} mapped guides, {len(commands)} distinct evidence commands' +
          (' executed.' if smoke else ' inventoried.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    try:
        check(args.smoke)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f'Curriculum check failed: {error}\n')
