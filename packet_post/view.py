"""Keyboard-driven tcod console. Only public game views are drawn."""

from __future__ import annotations

import copy
import textwrap
import unicodedata
from pathlib import Path

from . import content

ASSETS = Path(__file__).with_name("assets")
INK = (233, 224, 202)
MUTED = (154, 176, 179)
GOLD = (246, 193, 94)
MINT = (139, 219, 182)
PAPER = (22, 34, 43)
PANEL = (32, 48, 57)


def ascii_text(text):
    text = str(text).replace("→", "->").replace("—", "-").replace("–", "-").replace("’", "'")
    return unicodedata.normalize("NFKD", text).encode("ascii", "replace").decode()


def wrapped(text, width):
    return [row for line in ascii_text(text).splitlines() for row in
            (textwrap.wrap(line, max(1, width), replace_whitespace=False) or [""])]


def draw_text(console, x, y, text, width, height, color=INK):
    for offset, line in enumerate(wrapped(text, width)[:max(0, height)]):
        console.print(x=x, y=y + offset, text=line, fg=color)


def feedback_text(view):
    last = view["last"]
    result = last["result"]
    summary = "Factual match" if result["correct"] else "A useful revision awaits"
    support = "supported practice" if last["supported"] else "first unassisted practice attempt"
    text = f"{summary} | {support}\n\nYOUR PREDICTION\n"
    text += "\n".join(f"{k}: {v}" for k, v in last["values"].items())
    text += "\n\nCOMPARE WITH THE BOUNDED RESULT\n"
    text += "\n".join(f"{k}: {v}" for k, v in result["expected"].items())
    text += "\n\n" + result["explanation"]
    model = result.get("model", {})
    if "packet_bytes" in model:
        text += f"\n\nMODEL: {model['ipv4_header']} + {model['tcp_header']} + {last['values']['payload']} "
        text += f"= {model['packet_bytes']} IP bytes; MTU {model['mtu']}; fits: {model['fits']}."
    if "addressed_dependencies" in model:
        text += "\n\nTARGETED: " + (" ".join(model["addressed_dependencies"]) or "No selected dependency targets this failure.")
        text += "\nRESIDUAL: " + " ".join(model["residual_risk"])
    return text + "\n\nUNKNOWN: " + "; ".join(result["unknowns"])


class UI:
    def __init__(self, game, save):
        self.game, self.save = game, save
        self.menu = game.state["current"] is None or not game.available(game.state["current"])
        self.selection = 0
        self.focus = 0
        self.values = {}
        self.reason = ""
        self.modal = None
        self.modal_title = ""
        self.modal_kind = ""
        self.scroll = 0
        self.editing = None
        self.edit_buffer = ""
        self.notice = "All stamps are practice. The course keeps its own assessment."
        self.quit = False
        if game.state["current"] is not None:
            self.reset_form()

    def perform(self, function, *args):
        before = copy.deepcopy(self.game.state)
        try:
            result = function(*args)
            self.save.write(self.game)
            return True, result
        except (ValueError, OSError) as error:
            self.game.state = before
            self.show("Could not save this action", str(error))
            return False, None

    def show(self, title, text, kind="read"):
        self.modal_title, self.modal, self.modal_kind = title, text, kind
        self.scroll = 0

    def reset_form(self):
        draft = self.game.progress["draft"]
        self.values, self.reason, self.focus = copy.deepcopy(draft["values"]), draft["reason"], 0

    def rows(self):
        view = self.game.visible()
        if not view:
            return []
        if view["stage"] == "debrief":
            fields = [content.text_field(k, label) for k, label in (
                ("mechanism", "Explain the rule"), ("evidence", "Cite a decisive source or record"),
                ("uncertainty", "Name what remains unknown"), ("action", "Next check, owner and success condition"))]
        else:
            fields = view["scene"]["fields"]
        rows = []
        for field in fields:
            key = field["key"]
            if "options" in field:
                selected = self.values.get(key, [] if field.get("multiple") else "")
                for option in field["options"]:
                    checked = option in selected if field.get("multiple") else option == selected
                    rows.append(dict(kind="option", key=key, value=option, multiple=field.get("multiple", False),
                                     text=f"{'[x]' if checked else '[ ]'} {field['label']}: {option}"))
            else:
                rows.append(dict(kind="text", key=key, text=f"{field['label']}: {self.values.get(key, '[Enter to write]')}"))
        if view["stage"] == "decision":
            rows.append(dict(kind="reason", key="reason", text="My reason: " + (self.reason or "[Enter to write]")))
        rows.append(dict(kind="submit", text="[ COMMIT PREDICTION ]" if view["stage"] == "decision" else "[ SAVE REFLECTION & COLLECT STAMP ]"))
        return rows

    def activate(self):
        rows = self.rows()
        row = rows[self.focus % len(rows)]
        if row["kind"] == "option":
            if row["multiple"]:
                selected = self.values.setdefault(row["key"], [])
                if row["value"] in selected:
                    selected.remove(row["value"])
                else:
                    selected.append(row["value"])
            else:
                self.values[row["key"]] = row["value"]
            ok, _ = self.perform(self.game.draft, self.values, self.reason)
            if not ok:
                self.reset_form()
        elif row["kind"] in {"text", "reason"}:
            self.editing = row["key"]
            self.edit_buffer = self.reason if row["kind"] == "reason" else self.values.get(row["key"], "")
        else:
            function = self.game.reflect if self.game.progress["stage"] == "debrief" else self.game.commit
            args = (self.values,) if self.game.progress["stage"] == "debrief" else (self.values, self.reason)
            ok, _ = self.perform(function, *args)
            if ok:
                self.reset_form()

    def text(self, value):
        if self.editing is not None and self.modal is None:
            self.edit_buffer = (self.edit_buffer + "".join(c for c in value if c.isprintable()))[:1600]

    def keep_edit(self):
        values, reason = copy.deepcopy(self.values), self.reason
        if self.editing == "reason":
            reason = self.edit_buffer
        else:
            values[self.editing] = self.edit_buffer
        ok, _ = self.perform(self.game.draft, values, reason)
        if ok:
            self.values, self.reason, self.editing = values, reason, None
        return ok

    def close(self):
        if self.editing is None or self.keep_edit():
            self.quit = True

    def key(self, key):
        if self.modal is not None:
            if key == "ESCAPE":
                self.modal = None
            elif key == "ENTER" and self.modal_kind == "hint-confirm":
                ok, hint = self.perform(self.game.hint)
                if ok:
                    self.show("Supported practice - hint recorded", hint)
            elif self.modal_kind == "evidence" and key.isdigit():
                cards = self.game.visible()["scene"]["cards"]
                index = int(key) - 1
                if 0 <= index < len(cards):
                    ok, body = self.perform(self.game.inspect, cards[index]["id"])
                    if ok:
                        self.show(cards[index]["label"], body)
            elif key in {"DOWN", "PAGEDOWN", "UP", "PAGEUP", "HOME", "END"}:
                self.scroll = max(0, self.scroll + {"DOWN": 1, "PAGEDOWN": 12, "UP": -1, "PAGEUP": -12,
                                                   "HOME": -100000, "END": 100000}[key])
            return
        if self.editing is not None:
            if key == "ESCAPE":
                self.editing = None
            elif key == "BACKSPACE":
                self.edit_buffer = self.edit_buffer[:-1]
            elif key == "ENTER":
                self.keep_edit()
            return
        if key in {"F2", "F3", "F4"}:
            settings = self.game.state["settings"]
            name = {"F2": "plain", "F3": "contrast", "F4": "scale"}[key]
            def change():
                settings[name] = settings[name] % 3 + 1 if name == "scale" else not settings[name]
            self.perform(change)
            return
        if key == "?":
            self.show("Desk instructions - no answer exposure",
                "Arrows / Tab: choose a field or action. Enter / Space: select or edit.\n"
                "In an editor, Enter keeps the text; Escape cancels.\n"
                "E: evidence cards. H: optional learning hint (records support). J: journal.\n"
                "X: export journal. B: full decision board. R: retry after feedback.\n"
                "Escape: return to desk. Q at the desk: save and quit.\n"
                "F2: plain / whimsical tone. F3: high contrast. F4: font size.\n\n"
                "Nothing is timed. Reading and moving do not consume an attempt. All actions are offline.\n"
                "Choose the COMMIT action only after completing every field and your reason. "
                "Corrective feedback makes subsequent attempts supported practice. "
                "Reflections are saved for human review, not automatically graded.")
            return
        if key == "J":
            self.show("Your practice journal", self.game.journal())
            return
        if key == "X":
            try:
                self.show("Journal exported", str(self.save.export(self.game)))
            except (OSError, ValueError) as error:
                self.show("Export failed", str(error))
            return
        if self.menu:
            count = len(content.missions())
            if key in {"UP", "DOWN", "TAB", "BACKTAB"}:
                self.selection = (self.selection + (-1 if key in {"UP", "BACKTAB"} else 1)) % count
            if key.isdigit() and 0 <= int(key) - 1 < count:
                self.selection = int(key) - 1
                key = "ENTER"
            if key in {"ENTER", "SPACE"}:
                ok, _ = self.perform(self.game.start, content.missions()[self.selection]["id"])
                if ok:
                    self.menu = False
                    self.reset_form()
            if key in {"Q", "ESCAPE"}:
                self.close()
            return
        if key == "ESCAPE":
            self.menu = True
            return
        view = self.game.visible()
        stage = view["stage"]
        if key == "B":
            self.show("Logical decision board", "\n".join(view["scene"]["board"]))
        elif key == "E" and stage in {"decision", "feedback"}:
            self.show("Choose evidence - press its number", "\n\n".join(
                f"{i}. {c['label']}\n{c['category']} | {content.source_name(c)}"
                for i, c in enumerate(view["scene"]["cards"], 1)), "evidence")
        elif key == "H" and stage == "decision":
            self.show("Open learning help?", "This hint will be recorded as support for this decision. "
                      "It never costs a stamp. Enter: show hint. Escape: return without opening.", "hint-confirm")
        elif stage == "brief" and key in {"ENTER", "SPACE"}:
            self.perform(self.game.begin)
        elif stage == "feedback":
            if key == "V":
                self.show("Prediction and bounded result", feedback_text(view))
            elif key == "R":
                ok, _ = self.perform(self.game.retry)
                if ok:
                    self.reset_form()
            elif key in {"ENTER", "SPACE"}:
                ok, _ = self.perform(self.game.advance)
                if ok:
                    self.reset_form()
        elif stage in {"decision", "debrief"}:
            if key in {"UP", "DOWN", "TAB", "BACKTAB"}:
                self.focus = (self.focus + (-1 if key in {"UP", "BACKTAB"} else 1)) % len(self.rows())
            elif key in {"ENTER", "SPACE"}:
                self.activate()
        elif stage == "complete" and key in {"ENTER", "SPACE"}:
            self.menu = True

    def draw(self, console):
        w, h = console.width, console.height
        high = self.game.state["settings"]["contrast"]
        bg, fg = ((0, 0, 0), (255, 255, 255)) if high else (PAPER, INK)
        console.clear(fg=fg, bg=bg)
        console.draw_rect(0, 0, w, 3, ch=32, bg=PANEL)
        draw_text(console, 2, 1, "PACKET POST / THE NIGHT SHIFT", w - 18, 1, GOLD)
        draw_text(console, w - 13, 1, "[ PRACTICE ]", 12, 1, MINT)
        footer = "?: controls  J: journal  X: export  F2: tone  F3: contrast  F4: font"
        draw_text(console, 2, h - 2, footer, w - 4, 1, MUTED)
        if self.menu:
            self.draw_menu(console)
        else:
            self.draw_scene(console)
        if self.modal is not None or self.editing is not None:
            x, y, width, height = 2, 4, w - 4, h - 8
            console.draw_rect(x, y, width, height, ch=32, bg=PANEL)
            editor_visible = self.editing is not None and self.modal is None
            title = "Write: " + self.editing if editor_visible else self.modal_title
            draw_text(console, x + 2, y + 1, title, width - 4, 2, GOLD)
            if editor_visible:
                lines = wrapped(self.edit_buffer + "_", width - 4)
                lines = lines[-(height - 7):]
                instructions = "Enter: keep text  Esc: cancel  Backspace: erase (1600 chars max)"
            else:
                lines = wrapped(self.modal, width - 4)
                self.scroll = min(self.scroll, max(0, len(lines) - (height - 7)))
                lines = lines[self.scroll:self.scroll + height - 7]
                instructions = "Esc: close  Up/Down or PgUp/PgDn: scroll"
                if self.modal_kind == "evidence":
                    instructions = "Number: open source  Esc: cancel"
                elif self.modal_kind == "hint-confirm":
                    instructions = "Enter: show recorded hint  Esc: cancel"
            for index, line in enumerate(lines):
                console.print(x=x + 2, y=y + 4 + index, text=line, fg=fg)
            draw_text(console, x + 2, y + height - 2, instructions, width - 4, 1, MINT)

    def draw_menu(self, console):
        w, h = console.width, console.height
        draw_text(console, 3, 5, "WELCOME TO BRAMBLEWORKS", w - 6, 1, MINT)
        draw_text(console, 3, 7, "     ___       .----.\n @  /___\\  ->  |POST|    Keep the mail moving. Keep your claims grounded.\n/|\\ |___|      '----'", w - 6, 3, GOLD)
        draw_text(console, 3, 11, "Select a mission. Existing progress resumes; nothing rerolls.", w - 6, 2)
        capacity = max(1, (h - 24) // 2)
        start = max(0, self.selection - capacity + 1)
        for i in range(start, min(len(content.missions()), start + capacity)):
            mission = content.missions()[i]
            p = self.game.state["progress"].get(mission["id"])
            status = "NEW" if not p else "STAMPED" if p["stage"] == "complete" else "RESUME"
            if not self.game.available(mission["id"]):
                status = "AFTER COURSE REVIEW"
            line = f"{'>' if self.selection == i else ' '} {i + 1}. {mission['title']}  [{status}]"
            draw_text(console, 3, 13 + (i - start) * 2, line, w - 6, 1, GOLD if self.selection == i else INK)
        mission = content.missions()[self.selection]
        y = min(h - 9, 15 + len(content.missions()) * 2)
        draw_text(console, 3, y, mission["intro"], w - 6, 3, MUTED)
        draw_text(console, 3, h - 5, "Enter/1-9: begin or resume   Q: save and quit", w - 6, 1, MINT)
        draw_text(console, 3, h - 4, f"Postage stamps: {len(self.game.state['stamps'])} | Offline, untimed practice", w - 6, 1)

    def draw_scene(self, console):
        view = self.game.visible()
        w, h, stage = console.width, console.height, view["stage"]
        draw_text(console, 2, 4, view["mission"]["title"], w - 4, 1, GOLD)
        if stage == "brief":
            draw_text(console, 3, 7, view["mission"]["character"], w - 6, 2, MINT)
            if not self.game.state["settings"]["plain"]:
                draw_text(console, 3, 10, view["mission"]["flavor"], w - 6, 3, GOLD)
            draw_text(console, 3, 14, view["mission"]["intro"], w - 6, h - 21)
            draw_text(console, 3, h - 6, "Enter: begin   Esc: desk   ?: controls", w - 6, 1, MINT)
            return
        if stage == "complete":
            draw_text(console, 3, 8, "[ POSTAGE STAMP COLLECTED ]", w - 6, 2, MINT)
            draw_text(console, 3, 12, view["mission"]["stamp"], w - 6, 2, GOLD)
            draw_text(console, 3, 16, "Your explanation is saved for reflection or human review. "
                      "A stamp records practice completion; it is not a course grade.\n\n"
                      "Revisit your journal and linked lesson. Use a new save ID for another run; "
                      "repeating a known puzzle is still practice.", w - 6, h - 23)
            draw_text(console, 3, h - 6, "Enter: desk   J: journal   X: export", w - 6, 1, MINT)
            return
        draw_text(console, 2, 6, view["scene"]["title"] if stage != "debrief" else "A note for the next shift", w - 4, 1, MINT)
        prompt = view["scene"]["prompt"] if stage != "debrief" else "Explain, cite, qualify, then choose a next check. These four notes are not automatically graded."
        draw_text(console, 2, 8, prompt, w - 4, 5)
        if stage == "feedback":
            last = view["last"]
            result = last["result"]
            draw_text(console, 3, 13, feedback_text(view), w - 6, h - 20)
            draw_text(console, 3, h - 6, "V: full result   Enter: next   R: retry" if result["correct"] else "V: full result   R: revise   E: evidence", w - 6, 2, MINT)
            return
        wide = w >= 85 and stage != "debrief"
        x = 36 if wide else 3
        width = w - x - 3
        if wide:
            board = "\n".join(view["scene"]["board"])
            if self.values:
                board += "\n\nYOUR DRAFT (not an outcome)\n" + "\n".join(f"{k}: {v}" for k, v in self.values.items())
            draw_text(console, 2, 14, board, 32, h - 22, GOLD)
            draw_text(console, 2, h - 7, "B: full board\nE: evidence  H: hint", 32, 2, MUTED)
        rows = self.rows()
        self.focus %= len(rows)
        rendered, focus_line = [], 0
        for index, row in enumerate(rows):
            if index == self.focus:
                focus_line = len(rendered)
            lines = wrapped(("> " if index == self.focus else "  ") + row["text"], width)
            rendered.extend((line, index == self.focus) for line in lines)
            rendered.append(("", False))
        capacity = h - 20
        start = max(0, focus_line - capacity + 3)
        for offset, (line, focused) in enumerate(rendered[start:start + capacity]):
            console.print(x=x, y=14 + offset, text=line, fg=GOLD if focused else INK)
        draw_text(console, x, h - 5, "Arrows/Tab: move  Enter/Space: select", width, 1, MINT)
        draw_text(console, x, h - 4, f"Field {self.focus + 1}/{len(rows)} | Esc: desk | E: evidence", width, 1, MUTED)


def tileset():
    import tcod.tileset
    return tcod.tileset.load_tilesheet(ASSETS / "font.png", 16, 8, list(range(128)))


def run(game, save, *, frames=None, screenshot=None):
    import tcod.console
    import tcod.context
    import tcod.event
    ui = UI(game, save)
    with tcod.context.new(width=1056, height=660, tileset=tileset(),
                          title="Packet Post - The Night Shift", argv=[]) as context:
        context.sdl_window.start_text_input()
        counter = 0
        while not ui.quit:
            factor = {1: 1.0, 2: 1.5, 3: 2.0}[game.state["settings"]["scale"]]
            console = context.new_console(min_columns=64, min_rows=36, magnification=factor)
            ui.draw(console)
            context.present(console, keep_aspect=True)
            counter += 1
            if frames is not None and counter >= frames:
                if screenshot:
                    context.save_screenshot(str(screenshot))
                return
            for event in tcod.event.wait(timeout=0.05 if frames is not None else None):
                if isinstance(event, tcod.event.Quit):
                    ui.close()
                elif isinstance(event, tcod.event.TextInput):
                    ui.text(event.text)
                elif isinstance(event, tcod.event.KeyDown) and not event.repeat:
                    key = event.sym.name
                    key = {"RETURN": "ENTER", "KP_ENTER": "ENTER", "QUESTION": "?"}.get(key, key)
                    if key == "SLASH" and event.mod & tcod.event.Modifier.SHIFT:
                        key = "?"
                    if key == "TAB" and event.mod & tcod.event.Modifier.SHIFT:
                        key = "BACKTAB"
                    if key.startswith("N") and len(key) == 2 and key[1].isdigit():
                        key = key[1]
                    ui.key(key)
