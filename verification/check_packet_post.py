#!/usr/bin/env python3
"""Check the optional game renderer; --window exercises a real desktop context."""

import argparse
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from packet_post.game import Game, Save
from packet_post.view import UI, run, tileset


def check(window=False, output=None):
    import tcod.console
    font = tileset()
    assert (font.tile_width, font.tile_height) == (8, 10)
    with tempfile.TemporaryDirectory(prefix="packet post ") as temp:
        with Save("check", Path(temp)) as save:
            game = Game()
            ui = UI(game, save)
            for width, height in ((64, 36), (88, 44), (130, 65)):
                console = tcod.console.Console(width, height)
                ui.draw(console)
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
            for width, height in ((64, 36), (88, 44), (130, 65)):
                console = tcod.console.Console(width, height)
                ui.draw(console)
            if window:
                run(game, save, frames=3, screenshot=output)
    print("Packet Post renderer passed: keyboard actions, 3 layouts, bundled font" + (", desktop window." if window else "."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--window", action="store_true")
    parser.add_argument("--screenshot", type=Path)
    args = parser.parse_args()
    check(args.window, args.screenshot)
