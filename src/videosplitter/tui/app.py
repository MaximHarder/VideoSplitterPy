"""Main Textual wizard: Settings, Split-Profiles, Start Split."""

from __future__ import annotations

import shutil
import threading
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, OptionList, Select, Static
from textual.widgets.option_list import Option

from videosplitter.cli import Request, execute
from videosplitter.ffmpeg import ffprobe_bin, system_fonts
from videosplitter.planner import Profile
from videosplitter.store import (
    ConfigError,
    Settings,
    delete_profile,
    ensure,
    list_profiles,
    load_profile,
    load_settings,
    save_profile,
    save_settings,
)


def _root() -> Path:
    return ensure()


def _ffmpeg_ok(ffmpeg: str) -> bool:
    probe = ffprobe_bin(ffmpeg)
    return shutil.which(ffmpeg) is not None or Path(ffmpeg).is_file()


class MainMenu(Screen):
    BINDINGS = [("q", "app.quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield OptionList(
            Option("1. Settings", id="settings"),
            Option("2. Split-Profiles", id="profiles"),
            Option("3. Start Split", id="start"),
            id="menu",
        )
        yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id == "settings":
            self.app.push_screen(SettingsScreen())
        elif event.option_id == "profiles":
            self.app.push_screen(ProfilesScreen())
        elif event.option_id == "start":
            self.app.push_screen(StartScreen())


_BOOL = (("true", "true"), ("false", "false"))
_MODES = ("size", "fixed", "flexible", "parts")
_SHOT_FMT = ("jpg", "png", "webp")
_SHOT_TIMES = (
    "random frame of the part",
    "first frame of the part",
    "last frame of the part",
    "random frame of the video",
    "first frame of the video",
    "last frame of the video",
    "50% of the part",
    "0% of the part",
    "100% of the part",
    "50% of the video",
)


def _bool_select(value: bool, widget_id: str) -> Select[str]:
    return Select(_BOOL, value="true" if value else "false", allow_blank=False, id=widget_id)


def _bool_value(screen: Screen, widget_id: str) -> bool:
    return screen.query_one(f"#{widget_id}", Select).value == "true"


def _choice_select(options: tuple[str, ...], value: str, widget_id: str) -> Select[str]:
    opts = [(item, item) for item in options]
    if value not in options:
        opts.insert(0, (value, value))
    return Select(opts, value=value, allow_blank=False, id=widget_id)


def _choice_value(screen: Screen, widget_id: str) -> str:
    value = screen.query_one(f"#{widget_id}", Select).value
    if value is Select.NULL or value is None:
        raise ValueError(f"{widget_id} required")
    return str(value)


class SettingsScreen(Screen):
    def compose(self) -> ComposeResult:
        root = _root()
        s = load_settings(root)
        names = list_profiles(root)
        profile_opts = [(n, n) for n in names] or [("default", "default")]
        default_profile = s.default_profile if s.default_profile in names else profile_opts[0][1]
        yield Header()
        with Vertical(id="settings-body"):
            yield VerticalScroll(
                Label("Settings (saved to settings.yml)"),
                Label("FFmpeg path"),
                Input(s.ffmpeg, id="ffmpeg"),
                Label("Video extensions (comma-separated)"),
                Input(", ".join(s.extensions), id="extensions"),
                Label("Remove source"),
                _bool_select(s.remove_source, "remove_source"),
                Label("Temp dir"),
                Input(s.temp_dir, id="temp_dir"),
                Label("Replace existing"),
                _bool_select(s.replace_existing, "replace_existing"),
                Label("Output dir"),
                Input(s.output_dir, id="output_dir"),
                Label("Recursive search"),
                _bool_select(s.recursive_search, "recursive_search"),
                Label("Default profile"),
                Select(profile_opts, value=default_profile, allow_blank=False, id="default_profile"),
                id="settings-form",
            )
            yield Horizontal(
                Button("Save", id="save", variant="primary"),
                Button("Back", id="back"),
                id="settings-actions",
            )
            yield Static("", id="msg")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
            return
        if event.button.id != "save":
            return
        msg = self.query_one("#msg", Static)
        try:
            ffmpeg = self.query_one("#ffmpeg", Input).value.strip() or "ffmpeg"
            if not _ffmpeg_ok(ffmpeg):
                msg.update("FFmpeg/ffprobe not found. Set a valid ffmpeg path.")
                return
            ext = tuple(
                part.strip().lstrip(".")
                for part in self.query_one("#extensions", Input).value.split(",")
                if part.strip()
            )
            profile = self.query_one("#default_profile", Select).value
            if profile is Select.NULL or profile is None:
                profile = "default"
            settings = Settings(
                ffmpeg=ffmpeg,
                extensions=ext or ("mp4",),
                remove_source=_bool_value(self, "remove_source"),
                temp_dir=self.query_one("#temp_dir", Input).value.strip(),
                replace_existing=_bool_value(self, "replace_existing"),
                output_dir=self.query_one("#output_dir", Input).value.strip() or "{source_path}",
                recursive_search=_bool_value(self, "recursive_search"),
                default_profile=str(profile),
            )
            save_settings(_root(), settings)
            msg.update("Saved.")
        except (ConfigError, ValueError, OSError) as exc:
            msg.update(str(exc))


def _selected_profile_name(plist: OptionList) -> str | None:
    if plist.highlighted is None:
        return None
    try:
        return str(plist.get_option_at_index(plist.highlighted).id)
    except (AttributeError, IndexError):
        return None


class ProfilesScreen(Screen):
    def compose(self) -> ComposeResult:
        root = _root()
        names = list_profiles(root)
        yield Header()
        yield Vertical(
            Label("Split-Profiles — select a profile, then Open (or press Enter)"),
            OptionList(*[Option(name, id=name) for name in names], id="plist"),
            Horizontal(
                Button("Open", id="open", variant="primary"),
                Button("New from default", id="new"),
                Button("Delete", id="delete"),
                Button("Back", id="back"),
            ),
            Label("New profile name"),
            Input(id="new_name"),
            Static("", id="msg"),
        )
        yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id:
            self.app.push_screen(ProfileEditScreen(str(event.option_id)))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        root = _root()
        msg = self.query_one("#msg", Static)
        if event.button.id == "back":
            self.app.pop_screen()
            return
        if event.button.id == "open":
            name = _selected_profile_name(self.query_one("#plist", OptionList))
            if not name:
                msg.update("Select a profile.")
                return
            self.app.push_screen(ProfileEditScreen(name))
            return
        if event.button.id == "new":
            name = self.query_one("#new_name", Input).value.strip()
            if not name:
                msg.update("Enter a name.")
                return
            try:
                base = load_profile(root, "default")
                slug = save_profile(root, name, base)
                self.app.pop_screen()
                self.app.push_screen(ProfilesScreen())
                self.app.push_screen(ProfileEditScreen(slug))
            except ConfigError as exc:
                msg.update(str(exc))
            return
        if event.button.id == "delete":
            name = _selected_profile_name(self.query_one("#plist", OptionList))
            if not name:
                msg.update("Select a profile.")
                return
            if name == "default":
                msg.update("Cannot delete default.")
                return
            try:
                delete_profile(root, name)
                self.app.pop_screen()
                self.app.push_screen(ProfilesScreen())
            except ConfigError as exc:
                msg.update(str(exc))


class ProfileEditScreen(Screen):
    """View and edit one profile's fields."""

    def __init__(self, name: str) -> None:
        super().__init__()
        self.profile_name = name

    def compose(self) -> ComposeResult:
        p = load_profile(_root(), self.profile_name)
        yield Header()
        with Vertical(id="profile-body"):
            yield VerticalScroll(
                Label(f"Profile: {self.profile_name}"),
                Label("Mode"),
                _choice_select(_MODES, p.mode, "mode"),
                Label("Split size (MB)"),
                Input(str(p.size_mb), id="size_mb"),
                Label("Fixed part length (minutes)"),
                Input(str(p.minutes), id="minutes"),
                Label("Min part length (minutes)"),
                Input(str(p.min_part_minutes), id="min_part_minutes"),
                Label("Flexible min (minutes)"),
                Input(str(p.flex_min), id="flex_min"),
                Label("Flexible max (minutes)"),
                Input(str(p.flex_max), id="flex_max"),
                Label("Parts (count)"),
                Input(str(p.parts), id="parts"),
                Label("Name template"),
                Input(p.name_template, id="name_template"),
                Label("Create screenshot"),
                _bool_select(p.create_screenshot, "create_screenshot"),
                Label("Screenshot time"),
                _choice_select(_SHOT_TIMES, p.screenshot_time, "screenshot_time"),
                Label("Screenshot name template"),
                Input(p.screenshot_name, id="screenshot_name"),
                Label("Screenshot format"),
                _choice_select(_SHOT_FMT, p.screenshot_format, "screenshot_format"),
                Label("Write label"),
                _bool_select(p.write_label, "write_label"),
                Label("Label template"),
                Input(p.label_template, id="label_template"),
                Label("Label font"),
                _choice_select(system_fonts() or (p.label_font,), p.label_font, "label_font"),
                Label("Label size (px)"),
                Input(str(p.label_size_px), id="label_size_px"),
                Label("Label color"),
                Input(p.label_color, id="label_color"),
                Label("Label position vertical (top/bottom:N)"),
                Input(
                    next((f"{k}:{v}" for k, v in p.label_position if k in {"top", "bottom"}), "bottom:15"),
                    id="pos_v",
                ),
                Label("Label position horizontal (left/right:N)"),
                Input(
                    next((f"{k}:{v}" for k, v in p.label_position if k in {"left", "right"}), "right:10"),
                    id="pos_h",
                ),
                Label("Label border size (px)"),
                Input(str(p.label_border_px), id="label_border_px"),
                Label("Label border color"),
                Input(p.label_border_color, id="label_border_color"),
                id="profile-form",
            )
            yield Horizontal(
                Button("Save", id="save", variant="primary"),
                Button("Back", id="back"),
                id="profile-actions",
            )
            yield Static("", id="msg")
        yield Footer()

    def _parse_side(self, raw: str, allowed: set[str]) -> tuple[str, int]:
        text = raw.strip()
        if ":" not in text:
            raise ValueError(f"use side:px, got {raw!r}")
        side, _, num = text.partition(":")
        side = side.strip().lower()
        if side not in allowed:
            raise ValueError(f"side must be one of {sorted(allowed)}")
        return side, int(num.strip())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
            return
        if event.button.id != "save":
            return
        msg = self.query_one("#msg", Static)
        try:
            pos_v = self._parse_side(self.query_one("#pos_v", Input).value, {"top", "bottom"})
            pos_h = self._parse_side(self.query_one("#pos_h", Input).value, {"left", "right"})
            profile = Profile(
                mode=_choice_value(self, "mode"),
                size_mb=float(self.query_one("#size_mb", Input).value),
                minutes=float(self.query_one("#minutes", Input).value),
                flex_min=float(self.query_one("#flex_min", Input).value),
                flex_max=float(self.query_one("#flex_max", Input).value),
                parts=int(float(self.query_one("#parts", Input).value)),
                min_part_minutes=float(self.query_one("#min_part_minutes", Input).value),
                name_template=self.query_one("#name_template", Input).value.strip(),
                create_screenshot=_bool_value(self, "create_screenshot"),
                screenshot_time=_choice_value(self, "screenshot_time"),
                screenshot_name=self.query_one("#screenshot_name", Input).value.strip(),
                screenshot_format=_choice_value(self, "screenshot_format"),
                write_label=_bool_value(self, "write_label"),
                label_template=self.query_one("#label_template", Input).value.strip(),
                label_font=_choice_value(self, "label_font"),
                label_size_px=int(float(self.query_one("#label_size_px", Input).value)),
                label_color=self.query_one("#label_color", Input).value.strip(),
                label_position=(pos_v, pos_h),
                label_border_px=int(float(self.query_one("#label_border_px", Input).value)),
                label_border_color=self.query_one("#label_border_color", Input).value.strip(),
            )
            save_profile(_root(), self.profile_name, profile)
            msg.update("Saved.")
        except (ConfigError, ValueError, TypeError) as exc:
            msg.update(str(exc))


class StartScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self._busy = False

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        for widget_id in ("preview", "run", "back"):
            self.query_one(f"#{widget_id}", Button).disabled = busy

    def _finish(self, text: str) -> None:
        self._set_busy(False)
        self.query_one("#msg", Static).update(text)

    def compose(self) -> ComposeResult:
        root = _root()
        settings = load_settings(root)
        names = list_profiles(root)
        options = [(n, n) for n in names] or [("default", "default")]
        yield Header()
        yield Vertical(
            Label("Start Split"),
            Label("Path (file or folder)"),
            Input(id="path"),
            Label("Profile"),
            Select(options, value=settings.default_profile if settings.default_profile in names else options[0][1], id="profile"),
            Horizontal(
                Button("Preview", id="preview", variant="primary"),
                Button("Run", id="run"),
                Button("Back", id="back"),
            ),
            Static("", id="summary"),
            Static("", id="msg"),
        )
        yield Footer()

    def _request(self) -> tuple[Request | None, str]:
        root = _root()
        settings = load_settings(root)
        if not _ffmpeg_ok(settings.ffmpeg):
            return None, "FFmpeg/ffprobe not found. Set path in Settings."
        raw = self.query_one("#path", Input).value.strip()
        if not raw:
            return None, "Path is required."
        path = Path(raw)
        if not path.exists():
            return None, "path not found"
        profile = self.query_one("#profile", Select).value
        if profile is Select.BLANK or profile is None:
            profile = settings.default_profile
        bulk = path.is_dir()
        sub = settings.recursive_search if bulk else None
        return (
            Request(path, bulk, sub, None, str(profile), None, None, None, None, None, None),
            "",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if self._busy:
            return
        if event.button.id == "back":
            self.app.pop_screen()
            return
        summary = self.query_one("#summary", Static)
        msg = self.query_one("#msg", Static)
        request, err = self._request()
        if err:
            msg.update(err)
            return
        assert request is not None
        root = _root()
        settings = load_settings(root)
        from videosplitter.cli import collect

        files = collect(
            request.path,  # type: ignore[arg-type]
            bulk=request.bulk,
            subfolders=bool(request.subfolders) if request.subfolders is not None else settings.recursive_search,
            extensions=settings.extensions,
        )
        if event.button.id == "preview":
            summary.update(
                f"Profile: {request.profile_name or settings.default_profile}\n"
                f"Files: {len(files)}\n"
                f"Recursive: {settings.recursive_search if request.bulk else False}\n"
                f"Confirm with Run."
            )
            msg.update("")
            return
        if event.button.id == "run":
            if not files and request.bulk:
                msg.update("no videos")
                return
            self._set_busy(True)
            summary.update("")
            msg.update("Running...")
            state = {"files": "", "parts": "", "log": []}

            def on_progress(line: str) -> None:
                if line.startswith("files:"):
                    state["files"] = line
                elif line.startswith("parts:"):
                    state["parts"] = line
                else:
                    state["log"].append(line)
                text = "\n".join(item for item in (state["files"], state["parts"], *state["log"]) if item)
                self.app.call_from_thread(summary.update, text)

            def work() -> None:
                try:
                    code = execute(request, on_progress=on_progress)
                    text = f"Finished with exit code {code}."
                except Exception as exc:
                    text = str(exc)
                self.app.call_from_thread(self._finish, text)

            threading.Thread(target=work, daemon=True).start()


class WizardApp(App[int]):
    TITLE = "videosplitter"
    CSS = """
    Screen { padding: 1 2; }
    #menu { width: 55; height: auto; border: solid $primary; }
    #settings-body, #profile-body { height: 1fr; }
    #settings-form, #profile-form { height: 1fr; }
    #settings-form Input, #settings-form Select, #profile-form Input, #profile-form Select { width: 100%; margin-bottom: 1; }
    #settings-actions, #profile-actions { height: auto; margin-top: 1; }
    """

    def on_mount(self) -> None:
        ensure()
        self.push_screen(MainMenu())


def run_tui() -> int:
    app = WizardApp()
    result = app.run()
    return int(result) if isinstance(result, int) else 0
