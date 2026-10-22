from pathlib import Path

import pytest

from videosplitter.store import ConfigError, config_dir, ensure, load_profile, load_settings, profile_slug


def test_config_dirs(tmp_path: Path):
    unix = config_dir({"XDG_CONFIG_HOME": str(tmp_path)}, "posix", tmp_path)
    assert unix == tmp_path / "videosplitter"
    fallback = config_dir({}, "posix", tmp_path)
    assert fallback == tmp_path / ".config" / "videosplitter"
    windows = config_dir({"APPDATA": str(tmp_path)}, "nt", tmp_path)
    assert windows == tmp_path / "videosplitter"


def test_round_trip(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    settings = load_settings(root)
    assert settings.ffmpeg == "ffmpeg"
    assert settings.extensions == ("mp4", "avi", "flv", "wmv", "mkv")
    assert settings.remove_source is False
    assert settings.temp_dir == "{source_path}/.temp"
    assert settings.replace_existing is True
    assert settings.output_dir == "{source_path}"
    assert settings.recursive_search is True
    assert settings.default_profile == "default"
    profile = load_profile(root, "default")
    assert profile.mode == "size"
    assert profile.size_mb == 1800
    assert profile.min_part_minutes == 8
    assert profile.minutes == 10
    assert profile.flex_min == 8
    assert profile.parts == 5
    assert profile.create_screenshot is False
    assert profile.screenshot_time == "random frame of the part"
    assert profile.screenshot_format == "jpg"
    assert profile.label_position == (("bottom", "15"), ("right", "10"))
    assert profile.label_bg is False
    assert profile.label_bg_shape == "parallelogram"
    text = (root / "profiles" / "default.yml").read_text(encoding="utf-8")
    (root / "profiles" / "default.yml").write_text(text, encoding="utf-8")
    assert load_profile(root, "default") == profile


def test_soft_merge_missing_keys(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    (root / "settings.yml").write_text("ffmpeg: custom\nextensions: [mp4]\nremove_source: false\n", encoding="utf-8")
    settings = load_settings(root)
    assert settings.ffmpeg == "custom"
    assert settings.recursive_search is True
    assert settings.replace_existing is True


def test_soft_merge_old_profile_gets_label_bg_defaults(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    path = root / "profiles" / "old.yml"
    # Minimal pre-0.2.0 profile without label_bg* keys
    lines = [
        line
        for line in (root / "profiles" / "default.yml").read_text(encoding="utf-8").splitlines()
        if not line.startswith("label_bg")
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    profile = load_profile(root, "old")
    assert profile.label_bg is False
    assert profile.label_bg_padding_x == "8"
    assert profile.label_bg_shape == "parallelogram"


def test_percent_position_round_trip(tmp_path: Path):
    from videosplitter.store import save_profile

    root = ensure(tmp_path / "cfg")
    profile = load_profile(root, "default")
    updated = profile.__class__(
        **{
            **profile.__dict__,
            "label_position": (("top", "50%"), ("left", "50%")),
            "label_bg_padding_x": "10%",
            "label_bg_padding_y": "5%",
        }
    )
    save_profile(root, "pct", updated)
    loaded = load_profile(root, "pct")
    assert loaded.label_position == (("top", "50%"), ("left", "50%"))
    assert loaded.label_bg_padding_x == "10%"
    assert loaded.label_bg_padding_y == "5%"


def test_invalid_percent_and_shape(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    path = root / "profiles" / "bad.yml"
    base = (root / "profiles" / "default.yml").read_text(encoding="utf-8")
    path.write_text(base.replace("bottom: 15", "bottom: 101%"), encoding="utf-8")
    with pytest.raises(ConfigError, match="profile cannot be parsed"):
        load_profile(root, "bad")
    path.write_text(base.replace("label_bg_shape: parallelogram", "label_bg_shape: chip"), encoding="utf-8")
    with pytest.raises(ConfigError, match="profile cannot be parsed"):
        load_profile(root, "bad")


def test_first_position_key_wins(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    path = root / "profiles" / "both.yml"
    path.write_text(
        (root / "profiles" / "default.yml").read_text(encoding="utf-8").replace(
            "bottom: 15\n  right: 10",
            "top: 1\n  bottom: 9\n  left: 2\n  right: 8",
        ),
        encoding="utf-8",
    )
    assert load_profile(root, "both").label_position == (("top", "1"), ("left", "2"))


def test_broken_yaml_is_left_in_place(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    path = root / "settings.yml"
    path.write_text("ffmpeg: [\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="settings cannot be parsed"):
        load_settings(root)
    assert path.read_text(encoding="utf-8") == "ffmpeg: [\n"


def test_profile_numbers_and_flexible_order(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    path = root / "profiles" / "default.yml"
    original = path.read_text(encoding="utf-8")
    path.write_text(original.replace("size_mb: 1800", "size_mb: 0"), encoding="utf-8")
    with pytest.raises(ConfigError, match="profile cannot be parsed"):
        load_profile(root, "default")
    path.write_text(
        original.replace("mode: size", "mode: flexible")
        .replace("flex_min: 8", "flex_min: 12")
        .replace("flex_max: 15", "flex_max: 10"),
        encoding="utf-8",
    )
    with pytest.raises(ConfigError, match="flexible minimum is greater than maximum"):
        load_profile(root, "default")


def test_missing_profile(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    with pytest.raises(ConfigError, match="profile not found"):
        load_profile(root, "missing")


def test_ensure_recreates_missing_default_profile(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    default = root / "profiles" / "default.yml"
    default.unlink()
    ensure(root)
    assert default.exists()


def test_profile_slug():
    assert profile_slug("My Profile") == "my-profile"


def test_tui_parse_side_accepts_percent():
    from videosplitter.tui.app import ProfileEditScreen

    assert ProfileEditScreen._parse_side(None, "top:50%", {"top", "bottom"}) == ("top", "50%")
    assert ProfileEditScreen._parse_side(None, "left:12", {"left", "right"}) == ("left", "12")

