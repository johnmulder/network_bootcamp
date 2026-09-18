"""Launch optional Packet Post practice without changing course sessions."""

from __future__ import annotations

import argparse
import sys

from . import content
from .game import Save


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", default="night-shift", help="local practice save name")
    parser.add_argument("--list", action="store_true", help="list missions without opening a window")
    parser.add_argument("--check", action="store_true", help="check practice content without tcod or a display")
    parser.add_argument("--export", action="store_true", help="export this save's journal without a display")
    parser.add_argument("--course-session", help="read current course reviews to unlock post-lesson incident/recovery practice")
    args = parser.parse_args(argv)
    try:
        if args.list:
            for mission in content.missions():
                suffix = " [after course review]" if mission.get("requires") else ""
                print(f"{mission['id']}: {mission['title']} ({mission['duration']}){suffix}")
            return 0
        if args.check:
            for scene in content.scenes().values():
                values = {f["key"]: scene.expected[f["key"]].split(", ") if f.get("multiple") else scene.expected[f["key"]]
                          for f in scene.fields}
                if not content.evaluate(scene, values)["correct"]:
                    raise ValueError("Invalid authored answer: " + scene.id)
                for card in scene.cards:
                    content.evidence(card)
            print(f"Packet Post content verified: {len(content.missions())} missions, {len(content.scenes())} decisions.")
            return 0
        if not args.export:
            try:
                import tcod  # noqa: F401 - check the optional runtime only when launching
            except ImportError:
                raise ValueError("Install optional game tools with: python3 -m venv work/game-venv; "
                                 "work/game-venv/bin/python -m pip install -r requirements-game.txt; "
                                 "work/game-venv/bin/python -m packet_post") from None
        with Save(args.id) as save:
            game = save.load()
            if args.course_session:
                game.authorize(args.course_session)
            if args.export:
                print(save.export(game))
            else:
                from .view import run
                run(game, save)
        return 0
    except (ValueError, OSError, RuntimeError) as error:
        print(f"Packet Post: {error}", file=sys.stderr)
        print("Use --list / --check without a display, or launch from a local desktop. Existing saves are preserved.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
