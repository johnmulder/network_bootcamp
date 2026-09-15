from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "prerequisites" / "setup.sh"


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load_module("fixture_builder", "labs/build_fixtures.py")
COURSE = load_module("course_navigator", "course.py")
WORKBENCHES = {
    "module1": load_module(
        "module1_workbench",
        "modules/module-01-operational-networking/workbench/module1_workbench.py",
    ),
    "module2": load_module(
        "module2_workbench",
        "modules/module-02-network-architecture/workbench/module2_workbench.py",
    ),
    "module3": load_module(
        "module3_workbench",
        "modules/module-03-incident-response-and-integration/workbench/module3_workbench.py",
    ),
}
QUESTION_COUNTS = {"module1": 25, "module2": 30, "module3": 28}


class FixtureBuilderTests(unittest.TestCase):
    def test_packet_helpers_build_valid_structures(self):
        source_mac = "02:00:00:00:00:01"
        destination_mac = "02:00:00:00:00:02"
        source_ip = "192.0.2.1"
        destination_ip = "198.51.100.2"

        self.assertEqual(BUILDER.mac(source_mac), bytes.fromhex("020000000001"))
        self.assertEqual(BUILDER.ip(source_ip), bytes([192, 0, 2, 1]))

        frame = BUILDER.ethernet(source_mac, destination_mac, 0x0800, b"data")
        self.assertEqual(frame[:6], BUILDER.mac(destination_mac))
        self.assertEqual(frame[6:12], BUILDER.mac(source_mac))
        self.assertEqual(struct.unpack("!H", frame[12:14])[0], 0x0800)

        tagged = BUILDER.ethernet(
            source_mac, destination_mac, 0x0800, b"data", vlan=42
        )
        self.assertEqual(struct.unpack("!HHH", tagged[12:18]), (0x8100, 42, 0x0800))

        arp = BUILDER.arp(1, source_mac, source_ip, destination_mac, destination_ip)
        self.assertEqual(len(arp), 28)
        self.assertEqual(struct.unpack("!HHBBH", arp[:8]), (1, 0x0800, 6, 4, 1))

        ip_packet = BUILDER.ipv4(source_ip, destination_ip, 17, b"payload", 7, ttl=9)
        self.assertEqual(ip_packet[0], 0x45)
        self.assertEqual(ip_packet[8:10], bytes([9, 17]))
        self.assertEqual(struct.unpack("!H", ip_packet[2:4])[0], len(ip_packet))
        self.assertEqual(BUILDER.checksum(ip_packet[:20]), 0)

        udp = BUILDER.udp(source_ip, destination_ip, 1234, 53, b"query")
        self.assertEqual(struct.unpack("!HHH", udp[:6]), (1234, 53, len(udp)))
        udp_pseudo = (
            BUILDER.ip(source_ip)
            + BUILDER.ip(destination_ip)
            + struct.pack("!BBH", 0, 17, len(udp))
        )
        self.assertEqual(BUILDER.checksum(udp_pseudo + udp), 0)

        tcp = BUILDER.tcp(
            source_ip,
            destination_ip,
            1234,
            443,
            10,
            20,
            0x18,
            b"hello",
            b"\x02\x04\x05",
        )
        self.assertEqual(tcp[12] >> 4, 6)
        tcp_pseudo = (
            BUILDER.ip(source_ip)
            + BUILDER.ip(destination_ip)
            + struct.pack("!BBH", 0, 6, len(tcp))
        )
        self.assertEqual(BUILDER.checksum(tcp_pseudo + tcp), 0)

        query = BUILDER.dns_query(12, "example.test")
        response = BUILDER.dns_response(12, "example.test", destination_ip)
        self.assertEqual(struct.unpack("!H", query[:2])[0], 12)
        self.assertEqual(struct.unpack("!HH", response[4:8]), (1, 1))
        self.assertIn(BUILDER.dns_name("example.test"), response)
        self.assertIn(b"service.example.test", BUILDER.tls_client_hello("service.example.test"))

        icmp = BUILDER.icmp_fragmentation_needed(ip_packet, 1200)
        self.assertEqual(icmp[:2], b"\x03\x04")
        self.assertEqual(struct.unpack("!H", icmp[6:8])[0], 1200)
        self.assertEqual(BUILDER.checksum(icmp), 0)

        wrapped = BUILDER.ip_frame(
            source_mac,
            destination_mac,
            source_ip,
            destination_ip,
            17,
            udp,
            8,
            vlan=42,
        )
        self.assertEqual(struct.unpack("!HHH", wrapped[12:18]), (0x8100, 42, 0x0800))
        self.assertEqual(wrapped[18], 0x45)

    def test_capture_writes_pcap_headers_and_records(self):
        capture = BUILDER.Capture()
        capture.add(1.25, b"abc")
        capture.add(2.5, b"defg")
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "capture.pcap"
            capture.write(path)
            data = path.read_bytes()

        self.assertEqual(
            struct.unpack("<IHHIIII", data[:24]),
            (0xA1B2C3D4, 2, 4, 0, 0, 65535, 1),
        )
        self.assertEqual(struct.unpack("<IIII", data[24:40]), (1, 250000, 3, 3))
        self.assertEqual(data[40:43], b"abc")
        self.assertEqual(struct.unpack("<IIII", data[43:59]), (2, 500000, 4, 4))
        self.assertEqual(data[59:], b"defg")

    def test_build_creates_the_complete_valid_dataset(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            with mock.patch.object(BUILDER, "FIXTURES", fixtures):
                BUILDER.build()
                self.assertEqual(BUILDER.check(), [])
                manifest = json.loads((fixtures / "manifest.json").read_text())

        entries = manifest["files"]
        self.assertEqual(len(entries), 39)
        self.assertEqual(
            Counter(Path(entry["path"]).parts[0] for entry in entries),
            {
                "architecture": 7,
                "challenges": 8,
                "incident": 10,
                "network": 4,
                "pcaps": 3,
                "routing": 7,
            },
        )
        self.assertTrue(all(len(entry["sha256"]) == 64 for entry in entries))

    def test_check_reports_every_fixture_failure_class(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            with mock.patch.object(BUILDER, "FIXTURES", fixtures):
                self.assertIn("missing labs/fixtures/manifest.json", BUILDER.check()[0])
                BUILDER.build()

                stray = fixtures / "stray.txt"
                stray.write_text("unexpected")
                self.assertIn("untracked fixture stray.txt", BUILDER.check())
                stray.unlink()

                missing = fixtures / "network" / "ipv6.json"
                missing.unlink()
                self.assertIn("missing network/ipv6.json", BUILDER.check())
                BUILDER.build()

                invalid_json = fixtures / "architecture" / "components.json"
                invalid_json.write_text("{")
                errors = BUILDER.check()
                self.assertTrue(any("checksum mismatch" in error for error in errors))
                self.assertTrue(any("invalid JSON architecture/components.json" in error for error in errors))
                BUILDER.build()

                invalid_jsonl = fixtures / "architecture" / "failures.jsonl"
                invalid_jsonl.write_text("not-json\n")
                self.assertTrue(
                    any("invalid JSON failures.jsonl:1" in error for error in BUILDER.check())
                )
                BUILDER.build()

                invalid_pcap = fixtures / "pcaps" / "incident.pcap"
                invalid_pcap.write_bytes(b"bad")
                self.assertIn("invalid PCAP incident.pcap", BUILDER.check())

    def test_main_builds_checks_and_reports_corruption(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            with mock.patch.object(BUILDER, "FIXTURES", fixtures):
                stdout = io.StringIO()
                with mock.patch.object(sys, "argv", ["build_fixtures.py"]), contextlib.redirect_stdout(stdout):
                    self.assertEqual(BUILDER.main(), 0)
                self.assertIn("fixtures ready: 39 files", stdout.getvalue())

                with mock.patch.object(sys, "argv", ["build_fixtures.py", "--check"]):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(BUILDER.main(), 0)

                (fixtures / "network" / "dhcp.jsonl").write_text("not-json\n")
                stderr = io.StringIO()
                with mock.patch.object(sys, "argv", ["build_fixtures.py", "--check"]), contextlib.redirect_stderr(stderr):
                    self.assertEqual(BUILDER.main(), 1)
                self.assertIn("invalid JSON dhcp.jsonl:1", stderr.getvalue())


    def test_challenge_rounds_preserve_sources_and_capture_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            with mock.patch.object(BUILDER, "FIXTURES", fixtures):
                BUILDER.build()
                first_manifest = (fixtures / "manifest.json").read_bytes()
                BUILDER.build()
                self.assertEqual((fixtures / "manifest.json").read_bytes(), first_manifest)
            self.assertEqual(
                (fixtures / "challenges/transfer.pcap").read_bytes(),
                (fixtures / "pcaps/mtu-failure.pcap").read_bytes(),
            )
            expected = (
                {"incident/assets.json", "incident/siem.jsonl", "incident/flows.jsonl"},
                {"incident/dns.jsonl", "incident/endpoint.jsonl", "incident/auth.jsonl"},
                {"incident/firewall.jsonl", "incident/proxy.jsonl", "routing/vrfs.json"},
            )
            for number, sources in enumerate(expected, 1):
                packet = json.loads((fixtures / f"challenges/incident-round-{number}.json").read_text())
                self.assertEqual(set(packet), sources)
                for source, records in packet.items():
                    raw = (fixtures / source).read_text()
                    original = [json.loads(line) for line in raw.splitlines()] if source.endswith(".jsonl") else json.loads(raw)
                    self.assertEqual(records, original)

    def test_capstone_variants_change_forward_and_return_decisions(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / "fixtures"
            with mock.patch.object(BUILDER, "FIXTURES", fixtures):
                BUILDER.build()
            case_a = json.loads((fixtures / "challenges/case-a.json").read_text())
            case_b = json.loads((fixtures / "challenges/case-b.json").read_text())
        lookup = WORKBENCHES["module1"].best_vrf_route
        self.assertEqual(case_a["before"]["routes"]["corp-vpc"], case_a["after"]["routes"]["corp-vpc"])
        for state in ("before", "after"):
            self.assertIsNotNone(lookup("corp-vpc", case_a["flow"]["dst"], case_a[state]["routes"]))
        self.assertIsNotNone(lookup("on-prem", case_a["flow"]["src"], case_a["before"]["routes"]))
        self.assertIsNone(lookup("on-prem", case_a["flow"]["src"], case_a["after"]["routes"]))
        self.assertIsNotNone(lookup(case_b["before"]["ingress_vrf"], case_b["flow"]["dst"], case_b["routes"]))
        self.assertIsNone(lookup(case_b["after"]["ingress_vrf"], case_b["flow"]["dst"], case_b["routes"]))
        self.assertFalse(case_b["conditions"]["route_leaking"])
        for case in (case_a, case_b):
            self.assertTrue(case["conditions"]["route_tables_complete_for_this_flow"])
            times = [record["time"] for record in case["observations"]]
            self.assertEqual(times, sorted(times))
            self.assertEqual(len({record["id"] for record in case["observations"]}), len(times))
            self.assertTrue(case["limitations"])


class WorkbenchTests(unittest.TestCase):
    def test_structured_questions_and_evaluation_preserve_identity(self):
        identifiers = set()
        for workbench in WORKBENCHES.values():
            for items in workbench.all_questions().values():
                for item in items:
                    self.assertNotIn(item["id"], identifiers)
                    identifiers.add(item["id"])
                    public = workbench.public_question(item)
                    self.assertEqual(set(public), {"id", "activity", "prompt", "evidence"})
                    json.dumps(public)
                    correct = workbench.evaluate_question(item, item["answer"])
                    self.assertTrue(correct["correct"])
                    wrong = workbench.evaluate_question(item, "intentionally wrong")
                    self.assertFalse(wrong["correct"])
                    self.assertNotIn("answer", wrong)
                    revealed = workbench.evaluate_question(item, item["answer"], revealed=True)
                    self.assertFalse(revealed["correct"])
                    self.assertEqual(revealed["learning_result"], "revealed")
            first = workbench.choose_questions("all", 3, None)
            second = workbench.choose_questions("all", 9, None)
            self.assertEqual({q["id"] for q in first}, {q["id"] for q in second})
        self.assertEqual(len(identifiers), 83)

    def test_existing_self_tests_and_question_contracts(self):
        for name, workbench in WORKBENCHES.items():
            with self.subTest(workbench=name):
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    self.assertEqual(workbench.self_test(), 0)
                self.assertIn(
                    f"self-test passed: {QUESTION_COUNTS[name]} questions",
                    stdout.getvalue(),
                )

                groups = workbench.all_questions()
                self.assertEqual(set(groups), set(workbench.ACTIVITIES))
                self.assertEqual(sum(map(len, groups.values())), QUESTION_COUNTS[name])
                for activity, questions in groups.items():
                    for item in questions:
                        self.assertEqual(item["activity"], activity)
                        self.assertEqual(
                            set(item),
                            {
                                "id",
                                "activity",
                                "prompt",
                                "answer",
                                "answers",
                                "explanation",
                                "evidence",
                            },
                        )
                        self.assertIn(workbench.normalize(item["answer"]), item["answers"])
                        self.assertTrue(item["evidence"])

    def test_question_selection_is_seeded_scoped_and_limited(self):
        for name, workbench in WORKBENCHES.items():
            with self.subTest(workbench=name):
                first = workbench.choose_questions("all", 17, 4)
                second = workbench.choose_questions("all", 17, 4)
                self.assertEqual(first, second)
                self.assertEqual(len(first), 4)

                activity = next(iter(workbench.ACTIVITIES))
                scoped = workbench.choose_questions(activity, 4, None)
                self.assertTrue(scoped)
                self.assertTrue(all(item["activity"] == activity for item in scoped))

                item = workbench.question(
                    activity,
                    "Prompt",
                    "YES, NOW",
                    "Explanation",
                    "fixture",
                    ("y -> now",),
                    question_id="test.normalize",
                )
                self.assertEqual(item["answers"], {"yes now", "y now"})

    def test_answer_display_handles_reveal_correct_wrong_and_eof(self):
        for name, workbench in WORKBENCHES.items():
            item = workbench.question("test", "Prompt", "yes", "Because", "fixture", ("y",), question_id="test.answer")
            with self.subTest(workbench=name, mode="reveal"):
                with mock.patch("builtins.input", side_effect=AssertionError("input called")):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertTrue(workbench.show_question(item, 1, True))
            with self.subTest(workbench=name, mode="correct"):
                with mock.patch("builtins.input", return_value=" Y "):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertTrue(workbench.show_question(item, 1, False))
            with self.subTest(workbench=name, mode="retry"):
                stdout = io.StringIO()
                with mock.patch("builtins.input", side_effect=("no", "Y")):
                    with contextlib.redirect_stdout(stdout):
                        self.assertTrue(workbench.show_question(item, 1, False))
                self.assertIn("Try once more", stdout.getvalue())
            with self.subTest(workbench=name, mode="help-and-show"):
                stdout = io.StringIO()
                with mock.patch("builtins.input", side_effect=("?", "show")):
                    with contextlib.redirect_stdout(stdout):
                        self.assertFalse(workbench.show_question(item, 1, False))
                self.assertIn("capitalization is ignored", stdout.getvalue())
                self.assertIn("Answer revealed", stdout.getvalue())
            with self.subTest(workbench=name, mode="wrong"):
                with mock.patch("builtins.input", return_value="no"):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertFalse(workbench.show_question(item, 1, False))
            with self.subTest(workbench=name, mode="eof"):
                with mock.patch("builtins.input", side_effect=EOFError):
                    with contextlib.redirect_stdout(io.StringIO()):
                        with self.assertRaisesRegex(SystemExit, "input ended"):
                            workbench.show_question(item, 1, False)

    def test_guided_practice_menu_defaults_to_a_short_mixed_session(self):
        for name, workbench in WORKBENCHES.items():
            with self.subTest(workbench=name):
                with mock.patch("builtins.input", return_value=""):
                    with mock.patch.object(workbench, "run_session", return_value=0) as run:
                        with contextlib.redirect_stdout(io.StringIO()):
                            self.assertEqual(workbench.main(["menu"]), 0)
                run.assert_called_once_with("all", 1, 5, False)

    def test_main_dispatches_all_common_cli_paths(self):
        for name, workbench in WORKBENCHES.items():
            activity = next(iter(workbench.ACTIVITIES))
            question = workbench.all_questions()[activity][0]
            with self.subTest(workbench=name, command="list"):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(workbench.main(["list"]), 0)
            with self.subTest(workbench=name, command="demo"):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(
                        workbench.main(["demo", activity, "--seed", "3", "--limit", "1"]),
                        0,
                    )
            with self.subTest(workbench=name, command="run"):
                with mock.patch.object(workbench, "choose_questions", return_value=[question]):
                    with mock.patch("builtins.input", return_value=question["answer"]):
                        with contextlib.redirect_stdout(io.StringIO()):
                            self.assertEqual(workbench.main(["run", activity, "--limit", "1"]), 0)
            with self.subTest(workbench=name, command="self-test"):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(workbench.main(["self-test"]), 0)
            with self.subTest(workbench=name, command="bad-limit"):
                with self.assertRaisesRegex(SystemExit, "limit must be at least 1"):
                    workbench.main(["demo", activity, "--limit", "0"])
            with self.subTest(workbench=name, command="required"):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        workbench.main([])
                self.assertEqual(raised.exception.code, 2)

    def test_manifest_verification_rejects_changed_dependencies(self):
        dependencies = {
            "module1": "network/l2-control.json",
            "module2": "architecture/components.json",
            "module3": "incident/assets.json",
        }
        for name, workbench in WORKBENCHES.items():
            with self.subTest(workbench=name):
                with tempfile.TemporaryDirectory() as temporary:
                    fixtures = Path(temporary) / "fixtures"
                    shutil.copytree(ROOT / "labs" / "fixtures", fixtures)
                    with mock.patch.object(workbench, "FIXTURES", fixtures):
                        workbench.verify_manifest()
                        path = fixtures / dependencies[name]
                        path.write_bytes(path.read_bytes() + b"changed")
                        with self.assertRaisesRegex(AssertionError, "checksum mismatch"):
                            workbench.verify_manifest()

    def test_module1_route_and_vrf_selection_boundaries(self):
        workbench = WORKBENCHES["module1"]
        rows = [
            {"prefix": "0.0.0.0/0", "preference": "1", "metric": "1", "next_hop": "default"},
            {"prefix": "10.0.0.0/24", "preference": "20", "metric": "1", "next_hop": "a"},
            {"prefix": "10.0.0.0/24", "preference": "10", "metric": "20", "next_hop": "b"},
            {"prefix": "10.0.0.0/24", "preference": "10", "metric": "5", "next_hop": "c"},
            {"prefix": "10.0.0.0/24", "preference": "10", "metric": "5", "next_hop": "d"},
        ]
        selected = workbench.select_routes("10.0.0.8", rows)
        self.assertEqual([row["next_hop"] for row in selected], ["c", "d"])
        self.assertEqual(workbench.select_routes("203.0.113.1", rows)[0]["next_hop"], "default")
        self.assertEqual(workbench.select_routes("203.0.113.1", rows[1:]), [])

        tables = {
            "TEST": [
                {"prefix": "0.0.0.0/0", "next_hop": "default"},
                {"prefix": "10.0.0.0/24", "next_hop": "specific"},
            ],
            "EMPTY": [],
        }
        self.assertEqual(
            workbench.best_vrf_route("TEST", "10.0.0.8", tables)["next_hop"],
            "specific",
        )
        self.assertIsNone(workbench.best_vrf_route("EMPTY", "10.0.0.8", tables))

    def test_module2_cloud_route_selection_boundaries(self):
        workbench = WORKBENCHES["module2"]
        data = {
            "attachments": {"app": "app-routes"},
            "routes": {
                "app-routes": [
                    {"prefix": "0.0.0.0/0", "target": "default"},
                    {"prefix": "10.0.0.0/24", "target": "specific"},
                ]
            },
        }
        table, route = workbench.cloud_route("app", "10.0.0.8", data)
        self.assertEqual(table, "app-routes")
        self.assertEqual(route["target"], "specific")
        data["routes"]["app-routes"] = []
        self.assertEqual(workbench.cloud_route("app", "10.0.0.8", data), ("app-routes", None))

    def test_convergence_uses_recorded_time_and_changed_prefix(self):
        workbench = WORKBENCHES["module1"]
        questions = workbench.convergence_questions()
        self.assertEqual([q["answer"] for q in questions], ["80", "10.255.0.3", "no", "10.0.20.0/24"])
        events = workbench.read_jsonl("routing/route-events.jsonl")
        next(event for event in events if event["event"] == "fib_install")["time"] = "2026-08-15T15:20:00.100Z"
        with mock.patch.object(workbench, "read_jsonl", return_value=events):
            self.assertEqual(workbench.convergence_questions()[0]["answer"], "100")

    def test_module3_transforms_and_filters_every_timeline_source(self):
        workbench = WORKBENCHES["module3"]
        logs = workbench.load_logs()
        events = workbench.build_timeline(logs)
        self.assertEqual(len(events), 17)
        self.assertEqual({event["source"] for event in events}, set(workbench.LOGS))
        self.assertEqual(
            events,
            sorted(events, key=lambda event: (workbench.parse_time(event["time"]), event["source"])),
        )
        for source, records in logs.items():
            with self.subTest(source=source):
                record = records[0]
                expected_time = record["start"] if source in {"flow", "vpn"} else record["time"]
                self.assertEqual(workbench.event_time(source, record), expected_time)
                self.assertTrue(workbench.event_entity(source, record))
                self.assertTrue(workbench.event_observation(source, record))

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(workbench.print_timeline("dns"), 0)
        self.assertIn(f"Events: {len(logs['dns'])} | Source: dns", stdout.getvalue())
        self.assertNotIn(" firewall ", stdout.getvalue())

    def test_python_entry_points_run_as_subprocesses(self):
        commands = [
            [sys.executable, "labs/build_fixtures.py", "--check"],
            [
                sys.executable,
                "modules/module-01-operational-networking/workbench/module1_workbench.py",
                "list",
            ],
            [
                sys.executable,
                "modules/module-02-network-architecture/workbench/module2_workbench.py",
                "list",
            ],
            [
                sys.executable,
                "modules/module-03-incident-response-and-integration/workbench/module3_workbench.py",
                "list",
            ],
        ]
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        for command in commands:
            with self.subTest(command=command[1]):
                result = subprocess.run(
                    command,
                    cwd=ROOT,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)


class CourseNavigatorTests(unittest.TestCase):
    def test_discovery_matches_the_complete_curriculum(self):
        self.assertEqual(len(COURSE.MODULES), 3)
        section_counts = []
        guide_counts = []
        for module in COURSE.MODULES:
            module_sections = COURSE.sections(module)
            section_counts.append(len(module_sections))
            guide_counts.append(sum(len(COURSE.guides(section)) for section in module_sections))
            self.assertEqual(len(COURSE.section_titles(module)), len(module_sections))
            self.assertTrue(COURSE.heading(module / "README.md").startswith("Module"))
        self.assertEqual(section_counts, [8, 8, 7])
        self.assertEqual(guide_counts, [43, 29, 32])

    def test_dashboard_module_and_section_are_concise_indexes(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(COURSE.main([]), 0)
        dashboard = stdout.getvalue()
        self.assertIn("Network Bootcamp", dashboard)
        self.assertIn("8 sections, 43 guides", dashboard)
        self.assertIn("7 sections, 32 guides", dashboard)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(COURSE.main(["module", "1"]), 0)
        module = stdout.getvalue()
        self.assertIn("Operational Networking", module)
        self.assertIn("1. Introduction and Mental Model (5 guides)", module)
        self.assertIn("8. Module 1 Review (1 guide)", module)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(COURSE.main(["section", "1", "2"]), 0)
        section = stdout.getvalue()
        self.assertIn("Layer 2 Networking", section)
        self.assertIn("1. Ethernet and MAC Addressing", section)
        self.assertIn("7. Layer 2 Packet-Path Exercise", section)

    def test_guide_prints_the_authoritative_markdown(self):
        path = COURSE.guide_path(3, 7, 3)
        expected = path.read_text(encoding="utf-8").rstrip()
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(COURSE.main(["guide", "3", "7", "3"]), 0)
        self.assertEqual(stdout.getvalue().rstrip(), expected)
        self.assertIn("# Completion Criteria and Capstone", expected)

    def test_guided_course_reaches_the_short_path_and_reference_library(self):
        with mock.patch.object(COURSE, "sys") as system:
            system.stdin.isatty.return_value = True
            system.stdout.isatty.return_value = True
            with mock.patch.object(COURSE, "guided_course", return_value=0) as guided:
                self.assertEqual(COURSE.main([]), 0)
        guided.assert_called_once_with()

        with mock.patch("builtins.input", side_effect=("", "q")):
            with mock.patch("delivery.cli", return_value=0) as learn:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(COURSE.guided_course(), 0)
        learn.assert_called_once_with(["learn"])

        answers = ("6", "", "b", "q")
        with mock.patch("builtins.input", side_effect=answers):
            with mock.patch.object(COURSE.pydoc, "pager") as pager:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(COURSE.guided_course(), 0)
        self.assertEqual(pager.call_count, 2)
        self.assertIn("# One-Day Network Bootcamp", pager.call_args_list[0].args[0])
        self.assertIn("# Be the Packet", pager.call_args_list[1].args[0])

        with mock.patch("builtins.input", side_effect=("2", "1", "1", "1", "m", "q")):
            with mock.patch.object(COURSE.pydoc, "pager") as pager:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(COURSE.guided_course(), 0)
        content = pager.call_args.args[0]
        self.assertIn("Module 1 — Operational Networking ›", content)
        self.assertIn("# Course Objectives and Shared Language", content)

    def test_day_and_challenge_commands_read_student_materials(self):
        self.assertEqual(len(COURSE.CHALLENGES), 6)
        for arguments, path in (
            (["day"], ROOT / "challenges/README.md"),
            (["challenge", "1"], COURSE.CHALLENGES[0]),
            (["challenge", "6"], COURSE.CHALLENGES[-1]),
        ):
            with self.subTest(arguments=arguments):
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    self.assertEqual(COURSE.main(arguments), 0)
                self.assertEqual(stdout.getvalue().rstrip(), path.read_text().rstrip())
        for number in (0, 7):
            with self.assertRaisesRegex(SystemExit, "challenge must be between 1 and 6"):
                COURSE.main(["challenge", str(number)])

    def test_invalid_numbers_and_missing_arguments_are_clear(self):
        cases = (
            (["module", "0"], "module must be between 1 and 3"),
            (["section", "1", "9"], "section must be between 1 and 8"),
            (["guide", "1", "8", "2"], "guide must be between 1 and 1"),
        )
        for arguments, message in cases:
            with self.subTest(arguments=arguments):
                with self.assertRaisesRegex(SystemExit, message):
                    COURSE.main(arguments)

        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                COURSE.main(["section", "1"])
        self.assertEqual(raised.exception.code, 2)

    def test_heading_errors_when_markdown_has_no_title(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "untitled.md"
            path.write_text("No heading here.\n")
            with self.assertRaisesRegex(SystemExit, "no # heading"):
                COURSE.heading(path)

    def test_practice_lists_or_translates_to_the_selected_workbench(self):
        with mock.patch.object(COURSE, "run_script", return_value=0) as run:
            self.assertEqual(COURSE.main(["practice", "1"]), 0)
            run.assert_called_once_with(COURSE.workbench_path(1), "list")

        with mock.patch.object(COURSE, "run_script", return_value=0) as run:
            self.assertEqual(
                COURSE.main(
                    [
                        "practice",
                        "2",
                        "cloud",
                        "--demo",
                        "--seed",
                        "7",
                        "--limit",
                        "4",
                    ]
                ),
                0,
            )
            run.assert_called_once_with(
                COURSE.workbench_path(2),
                "demo",
                "cloud",
                "--seed",
                "7",
                "--limit",
                "4",
            )

        with mock.patch.object(COURSE, "run_script", return_value=8) as run:
            self.assertEqual(COURSE.main(["practice", "3", "scope"]), 8)
            run.assert_called_once_with(
                COURSE.workbench_path(3), "run", "scope", "--seed", "1"
            )

        with self.assertRaisesRegex(SystemExit, "limit must be at least 1"):
            COURSE.main(["practice", "1", "routes", "--limit", "0"])

    def test_timeline_translates_source_and_preserves_status(self):
        with mock.patch.object(COURSE, "run_script", return_value=0) as run:
            self.assertEqual(COURSE.main(["timeline"]), 0)
            run.assert_called_once_with(COURSE.workbench_path(3), "timeline")

        with mock.patch.object(COURSE, "run_script", return_value=6) as run:
            self.assertEqual(COURSE.main(["timeline", "--source", "endpoint"]), 6)
            run.assert_called_once_with(
                COURSE.workbench_path(3), "timeline", "--source", "endpoint"
            )

    def test_verify_runs_every_check_and_reports_aggregate_status(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(COURSE, "run_script", side_effect=(0, 7, 0, 2, 0)) as run:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.assertEqual(COURSE.main(["verify"]), 7)
        self.assertEqual(run.call_count, 5)
        self.assertIn("== Evidence fixtures ==", stdout.getvalue())
        self.assertIn("== Public exemplars ==", stdout.getvalue())
        self.assertIn("== Module 3 workbench ==", stdout.getvalue())
        self.assertIn("Course verification failed", stderr.getvalue())

        stdout = io.StringIO()
        with mock.patch.object(COURSE, "run_script", return_value=0) as run:
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(COURSE.main(["verify"]), 0)
        self.assertEqual(run.call_count, 5)
        self.assertIn("Course verification passed", stdout.getvalue())

    def test_run_script_uses_python_and_preserves_exit_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            script = Path(temporary) / "exit.py"
            script.write_text("raise SystemExit(9)\n")
            self.assertEqual(COURSE.run_script(script, "unused"), 9)

    def test_entry_point_works_outside_the_repository(self):
        commands = (
            [sys.executable, str(ROOT / "course.py"), "module", "2"],
            [str(ROOT / "course"), "module", "2"],
        )
        for command in commands:
            with self.subTest(command=command[0]):
                with tempfile.TemporaryDirectory() as temporary:
                    result = subprocess.run(
                        command,
                        cwd=temporary,
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Module 2 — Network Architecture", result.stdout)


class SetupScriptTests(unittest.TestCase):
    formulae = ("python", "wireshark", "zeek", "jq", "iperf3")
    commands = (
        "cat",
        "column",
        "python3",
        "tshark",
        "zeek",
        "jq",
        "iperf3",
        "tcpdump",
        "netstat",
        "route",
        "arp",
        "traceroute",
        "nc",
    )

    @staticmethod
    def write_executable(path: Path, content: str) -> None:
        path.write_text(content)
        path.chmod(0o755)

    def run_setup(
        self,
        *arguments: str,
        platform: str = "Darwin",
        installed: tuple[str, ...] | None = None,
        missing_commands: tuple[str, ...] = (),
        old_python: bool = False,
    ) -> tuple[subprocess.CompletedProcess[str], str, str]:
        installed = self.formulae if installed is None else installed
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            binaries = directory / "bin"
            binaries.mkdir()
            brew_log = directory / "brew.log"
            python_log = directory / "python.log"
            brew_state = directory / "brew.state"
            brew_state.write_text("".join(f"{formula}\n" for formula in installed))

            self.write_executable(
                binaries / "uname",
                f"#!/bin/sh\nprintf '%s\\n' '{platform}'\n",
            )
            self.write_executable(
                binaries / "dirname",
                "#!/bin/sh\n/usr/bin/dirname \"$@\"\n",
            )
            self.write_executable(
                binaries / "brew",
                """#!/bin/sh
printf '%s\n' "$*" >> "$FAKE_BREW_LOG"
case "$1" in
    list)
        [ "$2" = "--versions" ] || exit 2
        /usr/bin/grep -qx "$3" "$FAKE_BREW_STATE" || exit 1
        printf '%s 1.0\n' "$3"
        ;;
    install)
        shift
        for formula do
            case "$formula" in
                python) executable=python3 ;;
                wireshark) executable=tshark ;;
                *) executable=$formula ;;
            esac
            printf '#!/bin/sh\n' > "$FAKE_BIN_DIR/$executable"
            /bin/chmod +x "$FAKE_BIN_DIR/$executable"
            printf '%s\n' "$formula" >> "$FAKE_BREW_STATE"
        done
        ;;
    *) exit 2 ;;
esac
""",
            )
            for command in self.commands:
                if command in missing_commands:
                    continue
                content = "#!/bin/sh\n"
                if command == "python3":
                    content += f'if [ "$1" = "-c" ]; then exit {int(old_python)}; fi\n'
                    content += "printf '%s\\n' \"$*\" >> \"$FAKE_PYTHON_LOG\"\n"
                self.write_executable(binaries / command, content)

            if "brew" in missing_commands:
                (binaries / "brew").unlink()
            environment = {
                **os.environ,
                "PATH": str(binaries),
                "FAKE_BREW_LOG": str(brew_log),
                "FAKE_BREW_STATE": str(brew_state),
                "FAKE_PYTHON_LOG": str(python_log),
                "FAKE_BIN_DIR": str(binaries),
            }
            result = subprocess.run(
                ["/bin/sh", str(SETUP), *arguments],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            return (
                result,
                brew_log.read_text() if brew_log.exists() else "",
                python_log.read_text() if python_log.exists() else "",
            )

    def test_shell_syntax(self):
        result = subprocess.run(
            ["/bin/sh", "-n", str(SETUP)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_unknown_arguments_and_non_macos_hosts(self):
        result, _, _ = self.run_setup("--unknown")
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)

        result, _, _ = self.run_setup(platform="Linux")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires macOS", result.stderr)

    def test_check_reports_missing_required_command_without_building(self):
        cases = (
            ({"missing_commands": ("jq",)}, "jq"),
            ({"missing_commands": ("tshark",)}, "wireshark"),
            ({"missing_commands": ("column",)}, "column"),
        )
        for options, missing in cases:
            with self.subTest(missing=missing):
                result, _, python_log = self.run_setup("--check", **options)
                self.assertEqual(result.returncode, 1)
                self.assertIn(f"{missing}", result.stdout)
                self.assertIn("prerequisites incomplete", result.stderr)
                self.assertEqual(python_log, "")

    def test_successful_check_verifies_fixtures(self):
        result, brew_log, python_log = self.run_setup("--check", installed=(), missing_commands=("zeek", "iperf3"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("prerequisites ready", result.stdout)
        self.assertIn("next: ./course", result.stdout)
        self.assertEqual(brew_log, "")
        self.assertEqual(
            python_log.strip(),
            f"{ROOT}/labs/build_fixtures.py --check",
        )

    def test_install_adds_only_missing_core_commands_then_checks_fixtures(self):
        result, brew_log, python_log = self.run_setup(installed=("python", "jq"), missing_commands=("tshark", "zeek", "iperf3"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(brew_log.splitlines(), ["install wireshark"])
        self.assertEqual(python_log.strip(), f"{ROOT}/labs/build_fixtures.py --check")
        self.assertIn("prerequisites ready", result.stdout)

    def test_extended_tools_are_checked_and_installed_only_when_requested(self):
        result, brew_log, _ = self.run_setup("--extended", "--check", missing_commands=("zeek",))
        self.assertEqual(result.returncode, 1)
        self.assertIn("zeek", result.stdout)
        self.assertEqual(brew_log, "")
        result, brew_log, _ = self.run_setup("--extended", missing_commands=("zeek", "iperf3"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(brew_log.splitlines(), ["install zeek iperf3"])

    def test_optional_live_tools_do_not_block_offline_delivery(self):
        result, brew_log, python_log = self.run_setup("--check", missing_commands=("nc", "tcpdump", "zeek", "iperf3"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unavailable (optional live exercise)", result.stdout)
        self.assertEqual(brew_log, "")
        self.assertIn("--check", python_log)

    def test_unsupported_python_is_reported_and_queued_for_installation(self):
        result, brew_log, python_log = self.run_setup("--check", old_python=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("3.10+", result.stdout)
        self.assertEqual(python_log, "")
        result, brew_log, _ = self.run_setup(old_python=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(brew_log.splitlines(), ["install python"])

    def test_homebrew_is_only_required_for_missing_packages(self):
        result, _, _ = self.run_setup("--check", missing_commands=("brew",))
        self.assertEqual(result.returncode, 0, result.stderr)
        result, _, _ = self.run_setup(missing_commands=("brew", "jq"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Homebrew is required to install", result.stderr)


if __name__ == "__main__":
    unittest.main()
