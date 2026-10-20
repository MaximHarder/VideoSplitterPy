from pathlib import Path

import pytest

from videosplitter.cli import Request, answers_to_request, apply_override
from videosplitter.planner import plan
from videosplitter.store import ensure, load_profile


def test_command_and_wizard_same_plan(tmp_path: Path, monkeypatch):
    from tests.support import write_stub
    from videosplitter.cli import command, wizard

    root = ensure(tmp_path / "cfg")
    ffmpeg = write_stub(tmp_path / "bin")
    text = (root / "settings.yml").read_text(encoding="utf-8").replace(
        "ffmpeg: ffmpeg", f'ffmpeg: "{ffmpeg.as_posix()}"'
    )
    (root / "settings.yml").write_text(text, encoding="utf-8")
    profile = (root / "profiles" / "default.yml").read_text(encoding="utf-8").replace(
        "min_part_minutes: 8", "min_part_minutes: 0.01"
    )
    (root / "profiles" / "default.yml").write_text(profile, encoding="utf-8")
    monkeypatch.setenv("VIDEOSPLITTER_CONFIG", str(root))
    monkeypatch.setenv("VIDEOSPLITTER_STUB_LOG", str(tmp_path / "log"))
    monkeypatch.setenv("VIDEOSPLITTER_STUB_DURATION", "100")
    monkeypatch.delenv("VIDEOSPLITTER_STUB_FAIL", raising=False)
    source = tmp_path / "movie.mp4"
    source.write_bytes(b"0123456789")
    seen = []

    def spy(profile, duration, size):
        seen.append(plan(profile, duration, size))
        return []

    monkeypatch.setattr("videosplitter.cli.plan", spy)
    assert command(str(source), split_by="size", split_size=1e-7) == 0
    assert wizard([str(source), "", "y", "size", "1e-7", ""]) == 0
    assert seen[0] == seen[1]
    assert len(seen[0]) > 1


def test_argv_flags(tmp_path: Path, monkeypatch):
    from videosplitter.cli import app

    seen = []

    def spy(request, **kwargs):
        seen.append(request)
        return 0

    monkeypatch.setattr("videosplitter.cli.execute", spy)
    source = tmp_path / "movie.mp4"
    source.write_bytes(b"v")
    with pytest.raises(SystemExit) as caught:
        app(["-f", str(source), "--bulk", "-sf"], exit_on_error=False)
    assert caught.value.code == 0
    assert seen[0].bulk is True
    assert seen[0].subfolders is True


def test_flags_and_wizard_match(tmp_path: Path):
    root = ensure(tmp_path / "cfg")
    base = load_profile(root, "default")
    flags = Request(Path("movie.mp4"), False, None, "D:/out", "default", "size", 100, None, None, None, None)
    answers = answers_to_request(
        ["movie.mp4", "default", "y", "size", "100", "D:/out"],
        exists=lambda path: True,
        is_dir=lambda path: False,
    )
    assert answers == flags
    left = plan(apply_override(base, flags), 1000, 200 * 1024 * 1024)
    right = plan(apply_override(base, answers), 1000, 200 * 1024 * 1024)
    assert left == right
    assert len(left) == 2


def test_directory_wizard_sets_bulk():
    request = answers_to_request(
        ["vids", "y", "", "n", ""],
        exists=lambda path: True,
        is_dir=lambda path: True,
    )
    assert request.bulk is True
    assert request.subfolders is True
    assert request.profile_name is None
    assert request.output is None


def test_invalid_answer(tmp_path: Path, capsys):
    from videosplitter.cli import wizard

    folder = tmp_path / "vids"
    folder.mkdir()
    assert wizard([str(folder), "maybe"]) == 2
    assert "invalid answer" in capsys.readouterr().err


def test_empty_path_rejected(capsys):
    from videosplitter.cli import wizard

    assert wizard([""]) == 2
    captured = capsys.readouterr()
    assert "path not found" in captured.err


def test_bare_app_calls_wizard(monkeypatch):
    from videosplitter.cli import app

    called = []

    def spy():
        called.append(True)
        return 0

    monkeypatch.setattr("videosplitter.cli.wizard", spy)
    with pytest.raises(SystemExit) as caught:
        app([], exit_on_error=False)
    assert caught.value.code == 0
    assert called


def test_wizard_none_runs_tui(monkeypatch):
    from videosplitter.cli import wizard

    monkeypatch.setattr("videosplitter.tui.app.run_tui", lambda: 0)
    assert wizard() == 0
