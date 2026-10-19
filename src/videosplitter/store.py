"""YAML settings and profiles outside the package."""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

from videosplitter.planner import Profile

_PROFILE_KEYS = (
    "mode", "size_mb", "minutes", "flex_min", "flex_max", "parts",
    "min_part_minutes", "name_template", "create_screenshot", "screenshot_time",
    "screenshot_name", "screenshot_format", "write_label", "label_template",
    "label_font", "label_size_px", "label_color", "label_position",
    "label_border_px", "label_border_color",
)

DEFAULT_SETTINGS = """\
ffmpeg: ffmpeg
extensions:
  - mp4
  - avi
  - flv
  - wmv
  - mkv
remove_source: false
temp_dir: ""
replace_existing: false
output_dir: "{source_dir}"
default_profile: default
"""

DEFAULT_PROFILE = """\
mode: size
size_mb: 1800
minutes: 30
flex_min: 5
flex_max: 10
parts: 2
min_part_minutes: 1
name_template: "{video_name}_p{part|pad(2)}.{ext}"
create_screenshot: false
screenshot_time: "50% of the part"
screenshot_name: "{video_name}_p{part|pad(2)}"
screenshot_format: jpg
write_label: false
label_template: "{part},[is_final][/is_final],{file_name}"
label_font: "Times New Roman"
label_size_px: 13
label_color: white
label_position:
  bottom: 15
  right: 5
label_border_px: 2
label_border_color: black
"""


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Settings:
    ffmpeg: str
    extensions: tuple[str, ...]
    remove_source: bool
    temp_dir: str
    replace_existing: bool
    output_dir: str
    default_profile: str


def config_dir(environ: dict[str, str] | None = None, name: str | None = None, home: Path | None = None) -> Path:
    environ = os.environ if environ is None else environ
    name = os.name if name is None else name
    home = Path.home() if home is None else home
    if name == "nt":
        appdata = environ.get("APPDATA")
        if not appdata:
            raise ConfigError("settings cannot be parsed")
        return Path(appdata) / "videosplitter"
    base = environ.get("XDG_CONFIG_HOME") or str(home / ".config")
    return Path(base) / "videosplitter"


def temp_path(settings: Settings) -> Path:
    if settings.temp_dir == "":
        return Path(tempfile.gettempdir())
    return Path(settings.temp_dir)


def ensure(root: Path | None = None) -> Path:
    root = config_dir() if root is None else root
    settings = root / "settings.yml"
    default = root / "profiles" / "default.yml"
    if settings.exists():
        return root
    root.mkdir(parents=True, exist_ok=True)
    default.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(DEFAULT_SETTINGS, encoding="utf-8")
    if not default.exists():
        default.write_text(DEFAULT_PROFILE, encoding="utf-8")
    return root


def _load(path: Path, broken: str) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        raise ConfigError(broken) from None


def load_settings(root: Path) -> Settings:
    raw = _load(root / "settings.yml", "settings cannot be parsed")
    if not isinstance(raw, dict):
        raise ConfigError("settings cannot be parsed")
    try:
        return Settings(
            ffmpeg=str(raw["ffmpeg"]),
            extensions=tuple(str(item) for item in raw["extensions"]),
            remove_source=bool(raw["remove_source"]),
            temp_dir=str(raw["temp_dir"]),
            replace_existing=bool(raw["replace_existing"]),
            output_dir=str(raw["output_dir"]),
            default_profile=str(raw["default_profile"]),
        )
    except (KeyError, TypeError):
        raise ConfigError("settings cannot be parsed") from None


def _position(raw: object) -> tuple[tuple[str, int], ...]:
    if not isinstance(raw, dict):
        raise ConfigError("profile cannot be parsed")
    vertical = horizontal = False
    kept: list[tuple[str, int]] = []
    for key, value in raw.items():
        if key in {"top", "bottom"} and not vertical:
            kept.append((key, int(value)))
            vertical = True
        elif key in {"left", "right"} and not horizontal:
            kept.append((key, int(value)))
            horizontal = True
    return tuple(kept)


def _check(profile: Profile) -> None:
    if profile.mode not in {"size", "fixed", "flexible", "parts"}:
        raise ConfigError("profile cannot be parsed")
    if profile.mode == "size" and profile.size_mb <= 0:
        raise ConfigError("profile cannot be parsed")
    if profile.mode == "fixed" and profile.minutes <= 0:
        raise ConfigError("profile cannot be parsed")
    if profile.mode == "flexible":
        if profile.flex_min <= 0 or profile.flex_max <= 0:
            raise ConfigError("profile cannot be parsed")
        if profile.flex_min > profile.flex_max:
            raise ConfigError("flexible minimum is greater than maximum")
    if profile.mode == "parts" and profile.parts < 1:
        raise ConfigError("profile cannot be parsed")


def load_profile(root: Path, name: str) -> Profile:
    path = root / "profiles" / f"{name}.yml"
    if not path.is_file():
        raise ConfigError("profile not found")
    raw = _load(path, "profile cannot be parsed")
    if not isinstance(raw, dict) or any(key not in raw for key in _PROFILE_KEYS):
        raise ConfigError("profile cannot be parsed")
    try:
        profile = Profile(
            mode=str(raw["mode"]),
            size_mb=float(raw["size_mb"]),
            minutes=float(raw["minutes"]),
            flex_min=float(raw["flex_min"]),
            flex_max=float(raw["flex_max"]),
            parts=int(raw["parts"]),
            min_part_minutes=float(raw["min_part_minutes"]),
            name_template=str(raw["name_template"]),
            create_screenshot=bool(raw["create_screenshot"]),
            screenshot_time=str(raw["screenshot_time"]),
            screenshot_name=str(raw["screenshot_name"]),
            screenshot_format=str(raw["screenshot_format"]),
            write_label=bool(raw["write_label"]),
            label_template=str(raw["label_template"]),
            label_font=str(raw["label_font"]),
            label_size_px=int(raw["label_size_px"]),
            label_color=str(raw["label_color"]),
            label_position=_position(raw["label_position"]),
            label_border_px=int(raw["label_border_px"]),
            label_border_color=str(raw["label_border_color"]),
        )
    except (TypeError, ValueError):
        raise ConfigError("profile cannot be parsed") from None
    _check(profile)
    return profile
