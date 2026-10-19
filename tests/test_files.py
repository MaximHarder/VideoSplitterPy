import os
from pathlib import Path

from tests.support import write_stub
from videosplitter.cli import Request, execute
from videosplitter.store import ensure


def _ready(tmp_path: Path, *, remove: bool, replace: bool, shot: bool = False):
    root = ensure(tmp_path / "cfg")
    ffmpeg = write_stub(tmp_path / "bin")
    settings = (root / "settings.yml").read_text(encoding="utf-8")
    settings = settings.replace("ffmpeg: ffmpeg", f'ffmpeg: "{ffmpeg.as_posix()}"')
    settings = settings.replace("remove_source: false", f"remove_source: {str(remove).lower()}")
    settings = settings.replace("replace_existing: false", f"replace_existing: {str(replace).lower()}")
    settings = settings.replace('output_dir: "{source_dir}"', f'output_dir: "{(tmp_path / "out").as_posix()}"')
    (root / "settings.yml").write_text(settings, encoding="utf-8")
    profile = (root / "profiles" / "default.yml").read_text(encoding="utf-8")
    profile = profile.replace("mode: size", "mode: parts").replace("parts: 2", "parts: 2")
    profile = profile.replace("min_part_minutes: 1", "min_part_minutes: 0.01")
    if shot:
        profile = profile.replace("create_screenshot: false", "create_screenshot: true")
    (root / "profiles" / "default.yml").write_text(profile, encoding="utf-8")
    os.environ["VIDEOSPLITTER_STUB_LOG"] = str(tmp_path / "log")
    os.environ["VIDEOSPLITTER_STUB_DURATION"] = "10"
    os.environ.pop("VIDEOSPLITTER_STUB_FAIL", None)
    os.environ.pop("VIDEOSPLITTER_STUB_FAIL_FRAMES", None)
    source = tmp_path / "Holiday.mp4"
    source.write_bytes(b"video")
    return root, source


def test_writes_parts_and_can_remove_source(tmp_path: Path, capsys):
    root, source = _ready(tmp_path, remove=True, replace=False)
    code = execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root)
    assert code == 0
    assert (tmp_path / "out" / "Holiday_p01.mp4").is_file()
    assert (tmp_path / "out" / "Holiday_p02.mp4").is_file()
    assert not source.exists()
    assert capsys.readouterr().out.strip() == f"wrote {source}"


def test_replace_off_keeps_existing_and_source(tmp_path: Path):
    root, source = _ready(tmp_path, remove=True, replace=False)
    first = tmp_path / "out" / "Holiday_p01.mp4"
    first.parent.mkdir(parents=True)
    first.write_bytes(b"old")
    second = tmp_path / "out" / "Holiday_p02.mp4"
    second.write_bytes(b"old2")
    code = execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root)
    assert code == 0
    assert first.read_bytes() == b"old"
    assert second.read_bytes() == b"old2"
    assert source.exists()


def test_screenshot_png_name(tmp_path: Path):
    root, source = _ready(tmp_path, remove=False, replace=False, shot=True)
    text = (root / "profiles" / "default.yml").read_text(encoding="utf-8")
    text = text.replace("screenshot_format: jpg", "screenshot_format: png")
    (root / "profiles" / "default.yml").write_text(text, encoding="utf-8")
    kept = tmp_path / "out" / "Holiday_p01.png"
    kept.parent.mkdir(parents=True)
    kept.write_bytes(b"old")
    code = execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root, random_at=1)
    assert code == 0
    assert kept.read_bytes() == b"old"
    assert (tmp_path / "out" / "Holiday_p02.png").is_file()
    assert not (tmp_path / "out" / "Holiday_p01.jpg").exists()
    log = (tmp_path / "log").read_text(encoding="utf-8")
    assert "7.500000" in log
    assert "drawtext" not in log


def test_screenshot_failure_keeps_part_and_source(tmp_path: Path, capsys):
    root, source = _ready(tmp_path, remove=True, replace=False, shot=True)
    os.environ["VIDEOSPLITTER_STUB_FAIL_FRAMES"] = "1"
    code = execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root)
    assert code == 1
    assert (tmp_path / "out" / "Holiday_p01.mp4").is_file()
    assert source.exists()
    assert "screenshot failed" in capsys.readouterr().err
    os.environ.pop("VIDEOSPLITTER_STUB_FAIL_FRAMES", None)
