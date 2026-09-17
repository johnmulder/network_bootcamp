#!/usr/bin/env python3
"""Render tagged lesson Mermaid with a maintainer CLI, or check saved exports."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'diagrams'
MANIFEST = OUT / 'manifest.json'


def sources():
    found = {}
    for base in ('challenges', 'facilitator', 'modules', 'labs'):
        for path in (ROOT / base).rglob('*.md'):
            for match in re.finditer(r'<!-- diagram: ([a-z0-9-]+) -->\s*<details>.*?```mermaid\n(.*?)\n```', path.read_text(), re.S):
                ident, source = match.groups()
                if ident in found:
                    raise ValueError(f'Duplicate diagram: {ident}')
                if 'accTitle:' not in source or 'accDescr:' not in source:
                    raise ValueError(f'Missing accessibility description: {ident}')
                found[ident] = (str(path.relative_to(ROOT)), source + '\n')
    return found


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check():
    manifest = json.loads(MANIFEST.read_text())
    current = sources()
    if set(current) != set(manifest['diagrams']):
        raise ValueError('Diagram source inventory differs from exports')
    for ident, (path, source) in current.items():
        entry = manifest['diagrams'][ident]
        if entry['source'] != path or entry['source_sha256'] != sha(source.encode()):
            raise ValueError(f'Stale diagram source: {ident}')
        if set(entry['exports']) != {ident + '.svg', ident + '.dark.svg'}:
            raise ValueError(f'Missing light/dark export: {ident}')
        for name, digest in entry['exports'].items():
            data = (OUT / name).read_bytes()
            if sha(data) != digest or b'<svg' not in data or b'</svg>' not in data:
                raise ValueError(f'Changed or invalid export: {name}')
    print(f'Diagrams verified: {len(current)} sources and light/dark SVG exports.')


def render(cli, browser):
    version = subprocess.check_output([cli, '--version'], text=True).strip()
    manifest = dict(renderer=f'@mermaid-js/mermaid-cli {version}', diagrams={})
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    with tempfile.TemporaryDirectory(prefix='bootcamp-diagrams-') as temporary:
        temp = Path(temporary)
        config = temp / 'mermaid.json'
        config.write_text(json.dumps({'flowchart': {'htmlLabels': False, 'useMaxWidth': True},
                                      'fontFamily': 'Arial', 'securityLevel': 'strict'}))
        browser_config = temp / 'browser.json'
        browser_config.write_text(json.dumps({'executablePath': browser}) if browser else '{}')
        for ident, (path, source) in sorted(sources().items()):
            old = previous.get('diagrams', {}).get(ident)
            if (previous.get('renderer') == manifest['renderer'] and old
                    and old['source'] == path and old['source_sha256'] == sha(source.encode())
                    and all((OUT / name).is_file() and sha((OUT / name).read_bytes()) == digest
                            for name, digest in old['exports'].items())):
                manifest['diagrams'][ident] = old
                continue
            input_path = temp / (ident + '.mmd')
            input_path.write_text(source)
            entry = dict(source=path, source_sha256=sha(source.encode()), exports={})
            for theme, suffix, background in [('default', '', 'white'), ('dark', '.dark', '#181818')]:
                name = ident + suffix + '.svg'
                target = temp / name
                subprocess.run([cli, '-i', str(input_path), '-o', str(target), '-I', ident,
                                '-t', theme, '-b', background, '-w', '1600', '-c', str(config),
                                '-p', str(browser_config), '-q'], check=True, timeout=60)
                data = target.read_bytes()
                (OUT / name).write_bytes(data)
                entry['exports'][name] = sha(data)
            manifest['diagrams'][ident] = entry
            print(f'Rendered {ident}', flush=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
    check()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--cli', default=str(ROOT / 'work/mermaid/node_modules/.bin/mmdc'))
    parser.add_argument('--browser', help='local Chrome/Chromium executable, authoring only')
    args = parser.parse_args()
    try:
        render(args.cli, args.browser) if args.render else check()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f'Diagram check failed: {error}\n')
