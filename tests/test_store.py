from pathlib import Path

import pytest

from videosplitter.store import ConfigError, config_dir, ensure, load_profile, load_settings


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
    assert settings.temp_dir == ""
    assert settings.replace_existing is False
    assert settings.output_dir == "{source_dir}"
    assert settings.default_profile == "default"
    profile = load_profile(root, "default")
    assert profile.mode == "size"
    assert profile.size_mb == 1800
    assert profile.min_part_minutes == 1
    assert profile.create_screenshot is False
    assert profile.screenshot_time == "50% of the part"
    assert profile.screenshot_format == "jpg"
    assert profile.label_position == (("bottom", 15), ("right", 5))
    text = (root / "profiles" / "default.yml").read_text(encoding="utf-8")
    (root / "profiles" / "default.yml").write_text(text, encoding="utf-8")
    assert load_profile(root, "default") == profile


def test_first_position_key_wins(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    path = root / "profiles" / "both.yml"
    path.write_text(
        (root / "profiles" / "default.yml").read_text(encoding="utf-8").replace(
            "bottom: 15\n  right: 5",
            "top: 1\n  bottom: 9\n  left: 2\n  right: 8",
        ),
        encoding="utf-8",
    )
    assert load_profile(root, "both").label_position == (("top", 1), ("left", 2))


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
    path.write_text(original.replace("mode: size", "mode: flexible").replace("flex_min: 5", "flex_min: 12"), encoding="utf-8")
    with pytest.raises(ConfigError, match="flexible minimum is greater than maximum"):
        load_profile(root, "default")


def test_missing_profile(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    with pytest.raises(ConfigError, match="profile not found"):
        load_profile(root, "missing")


def test_present_settings_do_not_recreate_a_deleted_profile(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    default = root / "profiles" / "default.yml"
    default.unlink()
    ensure(root)
    assert not default.exists()
