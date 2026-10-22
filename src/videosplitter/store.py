"""YAML settings and profiles outside the package."""

from __future__ import annotations

import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

from videosplitter.names import translited
from videosplitter.planner import Profile

_PROFILE_KEYS = (
    "mode", "size_mb", "minutes", "flex_min", "flex_max", "parts",
    "min_part_minutes", "name_template", "create_screenshot", "screenshot_time",
    "screenshot_name", "screenshot_format", "write_label", "label_template",
    "label_font", "label_size_px", "label_color", "label_position",
    "label_border_px", "label_border_color",
    "label_bg", "label_bg_shape", "label_bg_color", "label_bg_padding_x",
    "label_bg_padding_y", "label_bg_skew_px", "label_bg_border_px",
    "label_bg_border_color",
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
temp_dir: "{source_path}/.temp"
replace_existing: true
output_dir: "{source_path}"
recursive_search: true
default_profile: default
"""

DEFAULT_PROFILE = """\
mode: size
size_mb: 1800
minutes: 10
flex_min: 8
flex_max: 15
parts: 5
min_part_minutes: 8
name_template: "{video_name|translited}_{part}.{ext}"
create_screenshot: false
screenshot_time: "random frame of the part"
screenshot_name: "{video_name|translited}_{part}"
screenshot_format: jpg
write_label: false
label_template: "[is_last]Final[else]PART {part|uppercase}[/is_last]"
label_font: "Times New Roman"
label_size_px: 13
label_color: white
label_position:
  bottom: 15
  right: 10
label_border_px: 2
label_border_color: black
label_bg: false
label_bg_shape: parallelogram
label_bg_color: white
label_bg_padding_x: "8"
label_bg_padding_y: "8"
label_bg_skew_px: 12
label_bg_border_px: 2
label_bg_border_color: black
"""

_SETTINGS_DEFAULTS = yaml.safe_load(DEFAULT_SETTINGS)


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
    recursive_search: bool
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


def expand_path_template(template: str, source_path: Path) -> Path:
    text = template.replace("{source_path}", str(source_path)).replace("{source_dir}", str(source_path))
    if text.strip() == "":
        return Path(tempfile.gettempdir())
    return Path(text)


def temp_path(settings: Settings, source_path: Path | None = None) -> Path:
    if settings.temp_dir.strip() == "":
        return Path(tempfile.gettempdir())
    if source_path is None and ("{source_path}" in settings.temp_dir or "{source_dir}" in settings.temp_dir):
        return Path(tempfile.gettempdir())
    if source_path is None:
        return Path(settings.temp_dir)
    return expand_path_template(settings.temp_dir, source_path)


def ensure(root: Path | None = None) -> Path:
    root = config_dir() if root is None else root
    root.mkdir(parents=True, exist_ok=True)
    (root / "profiles").mkdir(parents=True, exist_ok=True)
    settings = root / "settings.yml"
    default = root / "profiles" / "default.yml"
    if not settings.exists():
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
    merged = {**_SETTINGS_DEFAULTS, **raw}
    try:
        temp_dir = str(merged["temp_dir"]).replace("{source_dir}", "{source_path}")
        output_dir = str(merged["output_dir"]).replace("{source_dir}", "{source_path}")
        return Settings(
            ffmpeg=str(merged["ffmpeg"]),
            extensions=tuple(str(item) for item in merged["extensions"]),
            remove_source=bool(merged["remove_source"]),
            temp_dir=temp_dir,
            replace_existing=bool(merged["replace_existing"]),
            output_dir=output_dir,
            recursive_search=bool(merged["recursive_search"]),
            default_profile=str(merged["default_profile"]),
        )
    except (KeyError, TypeError):
        raise ConfigError("settings cannot be parsed") from None


def save_settings(root: Path, settings: Settings) -> None:
    data = {
        "ffmpeg": settings.ffmpeg,
        "extensions": list(settings.extensions),
        "remove_source": settings.remove_source,
        "temp_dir": settings.temp_dir,
        "replace_existing": settings.replace_existing,
        "output_dir": settings.output_dir,
        "recursive_search": settings.recursive_search,
        "default_profile": settings.default_profile,
    }
    path = root / "settings.yml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _length_token(raw: object) -> str:
    """Bare number = px; trailing % = fraction of frame axis (0–100)."""
    if isinstance(raw, bool):
        raise ConfigError("profile cannot be parsed")
    if isinstance(raw, (int, float)):
        if isinstance(raw, float) and not raw.is_integer():
            raise ConfigError("profile cannot be parsed")
        n = int(raw)
        if n < 0:
            raise ConfigError("profile cannot be parsed")
        return str(n)
    text = str(raw).strip()
    if text.endswith("%"):
        try:
            pct = float(text[:-1].strip())
        except ValueError:
            raise ConfigError("profile cannot be parsed") from None
        if pct < 0 or pct > 100:
            raise ConfigError("profile cannot be parsed")
        return f"{pct:g}%"
    try:
        value = float(text)
    except ValueError:
        raise ConfigError("profile cannot be parsed") from None
    if value < 0 or value != int(value):
        raise ConfigError("profile cannot be parsed")
    return str(int(value))


def _position(raw: object) -> tuple[tuple[str, str], ...]:
    if not isinstance(raw, dict):
        raise ConfigError("profile cannot be parsed")
    vertical = horizontal = False
    kept: list[tuple[str, str]] = []
    for key, value in raw.items():
        if key in {"top", "bottom"} and not vertical:
            kept.append((key, _length_token(value)))
            vertical = True
        elif key in {"left", "right"} and not horizontal:
            kept.append((key, _length_token(value)))
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
    if profile.label_bg_shape not in {"rect", "parallelogram"}:
        raise ConfigError("profile cannot be parsed")
    if profile.label_bg_skew_px < 0 or profile.label_bg_border_px < 0:
        raise ConfigError("profile cannot be parsed")
    _length_token(profile.label_bg_padding_x)
    _length_token(profile.label_bg_padding_y)


def profile_slug(name: str) -> str:
    slug = translited(name.strip(), space="-")
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", slug).strip("-").lower()
    if not slug:
        raise ConfigError("profile cannot be parsed")
    return slug


def _profile_defaults() -> dict:
    return yaml.safe_load(DEFAULT_PROFILE)


def load_profile(root: Path, name: str) -> Profile:
    path = root / "profiles" / f"{name}.yml"
    if not path.is_file():
        raise ConfigError("profile not found")
    raw = _load(path, "profile cannot be parsed")
    if not isinstance(raw, dict):
        raise ConfigError("profile cannot be parsed")
    merged = {**_profile_defaults(), **raw}
    if any(key not in merged for key in _PROFILE_KEYS):
        raise ConfigError("profile cannot be parsed")
    try:
        profile = Profile(
            mode=str(merged["mode"]),
            size_mb=float(merged["size_mb"]),
            minutes=float(merged["minutes"]),
            flex_min=float(merged["flex_min"]),
            flex_max=float(merged["flex_max"]),
            parts=int(merged["parts"]),
            min_part_minutes=float(merged["min_part_minutes"]),
            name_template=str(merged["name_template"]),
            create_screenshot=bool(merged["create_screenshot"]),
            screenshot_time=str(merged["screenshot_time"]),
            screenshot_name=str(merged["screenshot_name"]),
            screenshot_format=str(merged["screenshot_format"]),
            write_label=bool(merged["write_label"]),
            label_template=str(merged["label_template"]),
            label_font=str(merged["label_font"]),
            label_size_px=int(merged["label_size_px"]),
            label_color=str(merged["label_color"]),
            label_position=_position(merged["label_position"]),
            label_border_px=int(merged["label_border_px"]),
            label_border_color=str(merged["label_border_color"]),
            label_bg=bool(merged["label_bg"]),
            label_bg_shape=str(merged["label_bg_shape"]),
            label_bg_color=str(merged["label_bg_color"]),
            label_bg_padding_x=_length_token(merged["label_bg_padding_x"]),
            label_bg_padding_y=_length_token(merged["label_bg_padding_y"]),
            label_bg_skew_px=int(merged["label_bg_skew_px"]),
            label_bg_border_px=int(merged["label_bg_border_px"]),
            label_bg_border_color=str(merged["label_bg_border_color"]),
        )
    except (TypeError, ValueError, ConfigError):
        raise ConfigError("profile cannot be parsed") from None
    _check(profile)
    return profile


def save_profile(root: Path, name: str, profile: Profile) -> str:
    slug = profile_slug(name)
    path = root / "profiles" / f"{slug}.yml"
    _check(profile)
    pos = {side: value for side, value in profile.label_position}
    data = {
        "mode": profile.mode,
        "size_mb": profile.size_mb,
        "minutes": profile.minutes,
        "flex_min": profile.flex_min,
        "flex_max": profile.flex_max,
        "parts": profile.parts,
        "min_part_minutes": profile.min_part_minutes,
        "name_template": profile.name_template,
        "create_screenshot": profile.create_screenshot,
        "screenshot_time": profile.screenshot_time,
        "screenshot_name": profile.screenshot_name,
        "screenshot_format": profile.screenshot_format,
        "write_label": profile.write_label,
        "label_template": profile.label_template,
        "label_font": profile.label_font,
        "label_size_px": profile.label_size_px,
        "label_color": profile.label_color,
        "label_position": pos,
        "label_border_px": profile.label_border_px,
        "label_border_color": profile.label_border_color,
        "label_bg": profile.label_bg,
        "label_bg_shape": profile.label_bg_shape,
        "label_bg_color": profile.label_bg_color,
        "label_bg_padding_x": profile.label_bg_padding_x,
        "label_bg_padding_y": profile.label_bg_padding_y,
        "label_bg_skew_px": profile.label_bg_skew_px,
        "label_bg_border_px": profile.label_bg_border_px,
        "label_bg_border_color": profile.label_bg_border_color,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return slug


def list_profiles(root: Path) -> list[str]:
    folder = root / "profiles"
    if not folder.is_dir():
        return []
    return sorted(path.stem for path in folder.glob("*.yml"))


def delete_profile(root: Path, name: str) -> None:
    path = root / "profiles" / f"{name}.yml"
    if not path.is_file():
        raise ConfigError("profile not found")
    path.unlink()
