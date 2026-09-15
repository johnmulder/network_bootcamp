"""Pinned acquisition fails closed; shipped evidence has reproducible semantics."""

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('exemplars', ROOT / 'labs/exemplars/manage.py')
exemplars = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exemplars)


class ExemplarTests(unittest.TestCase):
    def test_offline_assets_and_frame_citations(self):
        exemplars.verify(decode=bool(shutil.which('tshark')))

    def test_changed_bytes_and_html_are_rejected(self):
        entry = json.loads((exemplars.ROOT / 'manifest.json').read_text())['files'][0]
        with self.assertRaisesRegex(ValueError, 'checksum'):
            exemplars.validate_bytes(entry, b'changed')
        html = b'<html>upstream error</html>'
        altered = dict(entry, bytes=len(html), sha256=hashlib.sha256(html).hexdigest())
        with self.assertRaisesRegex(ValueError, 'format'):
            exemplars.validate_bytes(altered, html)

    def test_missing_companion_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            for entry in json.loads((exemplars.ROOT / 'manifest.json').read_text())['files']:
                if entry['path'].endswith('.keys'):
                    continue
                shutil.copyfile(exemplars.ROOT / entry['path'], directory / entry['path'])
            with self.assertRaisesRegex(ValueError, 'Missing companion'):
                exemplars.verify(directory)

    def test_http_failure_keeps_existing_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp)
            sentinel = destination / 'tls13-rfc8446.pcap'
            sentinel.write_bytes(b'previous')
            with mock.patch.object(exemplars.subprocess, 'run', side_effect=subprocess.CalledProcessError(22, 'curl')) as run:
                with self.assertRaises(subprocess.CalledProcessError):
                    exemplars.fetch(destination)
            self.assertIn('--fail', run.call_args.args[0])
            self.assertEqual(sentinel.read_bytes(), b'previous')

    def test_bad_download_keeps_existing_assets(self):
        def html_download(args, **kwargs):
            Path(args[args.index('--output') + 1]).write_bytes(b'<html>error</html>')
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp)
            sentinel = destination / 'tls13-rfc8446.pcap'
            sentinel.write_bytes(b'previous')
            with mock.patch.object(exemplars.subprocess, 'run', side_effect=html_download):
                with self.assertRaisesRegex(ValueError, 'checksum'):
                    exemplars.fetch(destination)
            self.assertEqual(sentinel.read_bytes(), b'previous')
