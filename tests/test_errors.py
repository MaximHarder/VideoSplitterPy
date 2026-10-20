import os
from pathlib import Path

from tests.support import write_stub
from videosplitter.cli import Request, execute
from videosplitter.store import ensure


def test_exit_2_before_any_cut(tmp_path: Path, capsys):
    missing = execute(Request(tmp_path / "nope.mp4", False, False, None, None, None, None, None, None, None, None), config=tmp_path / "cfg")
    assert missing == 2
    assert "path not found" in capsys.readouterr().err
    folder = tmp_path / "vids"
    folder.mkdir()
    assert execute(Request(folder, False, False, None, None, None, None, None, None, None, None), config=tmp_path / "cfg") == 2
    assert "directory requires --bulk" in capsys.readouterr().err
    source = tmp_path / "a.mp4"
    source.write_bytes(b"v")
    assert execute(Request(source, True, False, None, None, None, None, None, None, None, None), config=tmp_path / "cfg") == 2
    assert "--bulk requires a directory" in capsys.readouterr().err
    assert execute(Request(source, False, True, None, None, None, None, None, None, None, None), config=tmp_path / "cfg") == 2
    assert "--subfolders requires --bulk" in capsys.readouterr().err


def test_bulk_subfolders_and_empty(tmp_path: Path, capsys):
    root = ensure(tmp_path / "cfg")
    ffmpeg = write_stub(tmp_path / "bin")
    text = (root / "settings.yml").read_text(encoding="utf-8").replace("ffmpeg: ffmpeg", f'ffmpeg: "{ffmpeg.as_posix()}"')
    text = text.replace('output_dir: "{source_path}"', f'output_dir: "{(tmp_path / "out").as_posix()}"')
    (root / "settings.yml").write_text(text, encoding="utf-8")
    profile = (root / "profiles" / "default.yml").read_text(encoding="utf-8")
    profile = profile.replace("mode: size", "mode: parts").replace("parts: 5", "parts: 2")
    profile = profile.replace("min_part_minutes: 8", "min_part_minutes: 0.01")
    profile = profile.replace(
        'name_template: "{video_name|translited}_{part}.{ext}"',
        'name_template: "{video_name}_p{part|pad(2)}.{ext}"',
    )
    (root / "profiles" / "default.yml").write_text(profile, encoding="utf-8")
    os.environ["VIDEOSPLITTER_STUB_LOG"] = str(tmp_path / "log")
    os.environ["VIDEOSPLITTER_STUB_DURATION"] = "10"
    os.environ.pop("VIDEOSPLITTER_STUB_FAIL", None)
    base = tmp_path / "vids"
    nested = base / "trip"
    nested.mkdir(parents=True)
    (nested / "clip.mp4").write_bytes(b"v")
    (base / "note.txt").write_bytes(b"no")
    assert execute(Request(base, True, False, None, None, None, None, None, None, None, None), config=root) == 0
    assert "no videos" in capsys.readouterr().out
    assert not (tmp_path / "out" / "trip" / "clip_p01.mp4").exists()
    code = execute(Request(base, True, True, None, None, None, None, None, None, None, None), config=root)
    assert code == 0
    assert (tmp_path / "out" / "trip" / "clip_p01.mp4").is_file()
    assert not (tmp_path / "out" / "note.txt").exists()
    empty = tmp_path / "empty"
    empty.mkdir()
    assert execute(Request(empty, True, False, None, None, None, None, None, None, None, None), config=root) == 0
    assert "no videos" in capsys.readouterr().out


def test_flexible_failure_continues(tmp_path: Path, capsys):
    root = ensure(tmp_path / "cfg")
    ffmpeg = write_stub(tmp_path / "bin")
    text = (root / "settings.yml").read_text(encoding="utf-8").replace("ffmpeg: ffmpeg", f'ffmpeg: "{ffmpeg.as_posix()}"')
    (root / "settings.yml").write_text(text, encoding="utf-8")
    profile = (root / "profiles" / "default.yml").read_text(encoding="utf-8")
    profile = profile.replace("mode: size", "mode: flexible").replace("flex_max: 15", "flex_max: 10")
    profile = profile.replace("min_part_minutes: 8", "min_part_minutes: 0.01")
    (root / "profiles" / "default.yml").write_text(profile, encoding="utf-8")
    os.environ["VIDEOSPLITTER_STUB_DURATION"] = str(11 * 60)
    os.environ["VIDEOSPLITTER_STUB_LOG"] = str(tmp_path / "log")
    folder = tmp_path / "vids"
    folder.mkdir()
    (folder / "a.mp4").write_bytes(b"a")
    (folder / "b.mp4").write_bytes(b"b")
    code = execute(Request(folder, True, False, str(tmp_path / "out"), None, None, None, None, None, None, None), config=root)
    assert code == 1
    err = capsys.readouterr().err
    assert "flexible bounds" in err
    assert err.count("fail ") == 2


def test_exit_2_messages(tmp_path: Path, capsys):
    root = ensure(tmp_path / "cfg")
    settings = (root / "settings.yml").read_text(encoding="utf-8")
    source = tmp_path / "a.mp4"
    source.write_bytes(b"v")
    assert execute(Request(source, False, False, None, "missing", None, None, None, None, None, None), config=root) == 2
    assert "profile not found" in capsys.readouterr().err
    profile = (root / "profiles" / "default.yml").read_text(encoding="utf-8")
    (root / "profiles" / "default.yml").write_text(
        profile.replace(
            'name_template: "{video_name|translited}_{part}.{ext}"',
            'name_template: "{nope}.{ext}"',
        ),
        encoding="utf-8",
    )
    assert execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root) == 2
    assert "unknown template" in capsys.readouterr().err
    (root / "profiles" / "default.yml").write_text(
        profile.replace("create_screenshot: false", "create_screenshot: true").replace(
            'screenshot_time: "random frame of the part"', 'screenshot_time: "101% of the part"'
        ),
        encoding="utf-8",
    )
    assert execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root) == 2
    assert "screenshot percent out of range" in capsys.readouterr().err
    (root / "profiles" / "default.yml").write_text(
        profile.replace("create_screenshot: false", "create_screenshot: true").replace(
            'screenshot_time: "random frame of the part"', 'screenshot_time: "noon"'
        ),
        encoding="utf-8",
    )
    assert execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root) == 2
    assert "unknown screenshot time" in capsys.readouterr().err
    (root / "settings.yml").write_text("ffmpeg: [\n", encoding="utf-8")
    assert execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root) == 2
    assert "settings cannot be parsed" in capsys.readouterr().err
    (root / "profiles" / "default.yml").write_text(profile, encoding="utf-8")
    (root / "settings.yml").write_text(settings, encoding="utf-8")
    assert execute(Request(source, False, False, None, None, "size", None, None, None, None, None), config=root) == 2
    assert "incomplete split override" in capsys.readouterr().err


def test_skip_and_keep_source(tmp_path: Path, capsys):
    root = ensure(tmp_path / "cfg")
    ffmpeg = write_stub(tmp_path / "bin")
    text = (root / "settings.yml").read_text(encoding="utf-8").replace("ffmpeg: ffmpeg", f'ffmpeg: "{ffmpeg.as_posix()}"')
    (root / "settings.yml").write_text(text, encoding="utf-8")
    os.environ["VIDEOSPLITTER_STUB_LOG"] = str(tmp_path / "log")
    os.environ["VIDEOSPLITTER_STUB_DURATION"] = "10"
    os.environ.pop("VIDEOSPLITTER_STUB_FAIL", None)
    source = tmp_path / "short.mp4"
    source.write_bytes(b"v")
    assert execute(Request(source, False, False, None, None, None, None, None, None, None, None), config=root) == 0
    captured = capsys.readouterr()
    assert "files:" in captured.err
    assert captured.out.strip() == f"skip {source}"
    assert source.exists()
