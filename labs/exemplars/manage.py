#!/usr/bin/env python3
"""Verify offline exemplars; --fetch explicitly reacquires pinned upstream bytes."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent


def validate_bytes(entry, data):
    if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
        raise ValueError(f"Size or checksum mismatch: {entry['path']}")
    content = gzip.decompress(data) if entry['format'] == 'pcapng+gzip' else data
    magic = {'pcap': b'\xd4\xc3\xb2\xa1', 'pcapng': b'\x0a\x0d\x0d\x0a',
             'pcapng+gzip': b'\x0a\x0d\x0d\x0a'}
    if entry['format'] in magic and not content.startswith(magic[entry['format']]):
        raise ValueError(f"Invalid capture format: {entry['path']}")


def verify(directory=ROOT, decode=False):
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    for entry in manifest['files']:
        validate_bytes(entry, (directory / entry['path']).read_bytes())
        for companion in entry.get('companions', []):
            if not (directory / companion).is_file():
                raise ValueError(f'Missing companion: {companion}')
        if decode and 'packets' in entry:
            result = subprocess.run(['tshark', '-n', '-r', str(directory / entry['path']),
                                     '-T', 'fields', '-e', 'frame.number'],
                                    check=True, capture_output=True, text=True, timeout=30)
            if len(result.stdout.splitlines()) != entry['packets']:
                raise ValueError(f"Packet count mismatch: {entry['path']}")
            for check in entry['checks']:
                args = ['tshark', '-n', '-r', str(directory / entry['path'])]
                if check.get('keylog'):
                    args += ['-o', f"tls.keylog_file:{directory / check['keylog']}"]
                args += ['-Y', check['filter'], '-T', 'fields', '-e', 'frame.number']
                result = subprocess.run(args, check=True, capture_output=True, text=True, timeout=30)
                if result.stdout.splitlines() != [str(n) for n in check['frames']]:
                    raise ValueError(f"Frame assertion failed: {entry['path']}: {check['filter']}")
    return manifest


def fetch(destination):
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    # Validate the entire set before replacing any local asset, including keys.
    with tempfile.TemporaryDirectory(prefix='bootcamp-exemplars-') as temporary:
        staging = Path(temporary)
        for entry in manifest['files']:
            subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                            '--proto', '=https', '--proto-redir', '=https', '--max-time', '60',
                            '--output', str(staging / entry['path']), entry['url']], check=True)
        verify(staging, decode=True)
        destination.mkdir(parents=True, exist_ok=True)
        for entry in manifest['files']:
            (destination / entry['path']).write_bytes((staging / entry['path']).read_bytes())


def fingerprint():
    digest = hashlib.sha256()
    for path in sorted(ROOT.iterdir()):
        if path.is_file():
            digest.update(path.name.encode() + b'\0' + path.read_bytes() + b'\0')
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--destination', type=Path, default=ROOT)
    parser.add_argument('--decode', action='store_true', help='also check TShark fields and frame numbers')
    args = parser.parse_args()
    try:
        if args.fetch:
            fetch(args.destination)
        manifest = verify(args.destination, decode=args.decode)
        print(f"Exemplars verified: {len(manifest['files'])} assets; network used only with --fetch.")
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(1, f'Exemplar verification failed: {error}\n')


if __name__ == '__main__':
    main()
