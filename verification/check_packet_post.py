#!/usr/bin/env python3
"""Check the optional game renderer; --window exercises a real desktop context."""

import argparse
import csv
import io
import json
import subprocess
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from packet_post.game import Game, Save
from packet_post.view import UI, run, tileset
from packet_post import content


def check(window=False, output=None):
    import tcod.console
    font = tileset()
    assert (font.tile_width, font.tile_height) == (8, 10)
    layouts = [(tcod.console.Console(w, h)) for w, h in ((64, 36), (88, 44), (130, 65))]

    def draw(ui, expected=None):
        for console in layouts:
            ui.draw(console)
            if expected:
                rendered = "\n".join("".join(chr(c) for c in row) for row in console.ch)
                assert expected in rendered, (console.width, console.height, expected)

    with tempfile.TemporaryDirectory(prefix="packet post ") as temp:
        with Save("check", Path(temp)) as save:
            game = Game()
            ui = UI(game, save)
            draw(ui)
            ui.key("ENTER")
            ui.key("ENTER")
            ui.key("E")
            ui.key("1")
            assert "route-candidates.csv" in ui.modal
            ui.key("ESCAPE")
            ui.key("H")
            ui.key("ESCAPE")
            assert not game.progress["help"]
            ui.key("H")
            ui.key("ENTER")
            assert game.progress["help"]["route.host"]
            ui.key("ESCAPE")
            draw(ui)
            if window:
                run(game, save, frames=3, screenshot=output)
        with Save("campaign", Path(temp)) as save:
            game = Game()
            # Synthetic release status tests rendering, never learner attainment.
            game.reviewed = {"c05.review", "c06.review", "exit.review"}
            ui = UI(game, save)
            for mission in content.missions():
                game.start(mission["id"])
                ui.menu = False
                draw(ui)
                game.begin()
                for step in mission["steps"]:
                    scene = content.scenes()[step]
                    ui.reset_form()
                    draw(ui)
                    ui.focus = len(ui.rows()) - 1
                    draw(ui, "COMMIT PREDICTION")
                    for item in scene.cards:
                        ui.show(item["label"], game.inspect(item["id"]))
                        draw(ui)
                        ui.key("END")
                        draw(ui)
                        ui.key("ESCAPE")
                    values = {f["key"]: scene.expected[f["key"]].split(", ") if f.get("multiple") else scene.expected[f["key"]]
                              for f in scene.fields}
                    game.commit(values, "Renderer verification, not learner evidence.")
                    draw(ui, "YOUR PREDICTION")
                    ui.key("V")
                    draw(ui)
                    ui.key("ESCAPE")
                    game.advance()
                ui.reset_form()
                draw(ui)
                game.reflect(dict(mechanism="Rule", evidence="Source", uncertainty="Scope", action="Next check"))
                draw(ui, "STAMP COLLECTED")
                ui.menu = True
                ui.selection = len(content.missions()) - 1
                draw(ui, "8.")
            ui.key("F3")
            draw(ui)
            save.write(game)
            assert save.load().state == game.state
    print("Packet Post renderer passed: 8 missions, 27 decisions, keyboard actions, 3 layouts, bundled font" + (", desktop window." if window else "."))


def decode():
    """Maintainer check only: recompute projections using the recorded commands."""
    observations = json.loads((ROOT / "packet_post/assets/observations.json").read_text())
    for ident, entry in observations.items():
        result = subprocess.run(entry["command"], cwd=ROOT, capture_output=True, text=True, check=True, timeout=30)
        if list(csv.DictReader(io.StringIO(result.stdout))) != entry["records"]:
            raise ValueError(f"Stored {ident} decoding differs from TShark output; inspect before updating.")
    print(f"Packet Post projections match TShark: {len(observations)} source captures.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", action="store_true")
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--content", action="store_true", help="verify content without installing tcod")
    parser.add_argument("--decode", action="store_true", help="verify saved decoder projections using local TShark")
    args = parser.parse_args()
    if args.content:
        from packet_post.__main__ import main
        raise SystemExit(main(["--check"]))
    elif args.decode:
        decode()
    else:
        check(args.window, args.screenshot)
