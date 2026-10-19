import os
from pathlib import Path

from tests.support import write_stub
from videosplitter.ffmpeg import ffprobe_bin, part_command, probe_duration, write_part


def test_sibling_probe():
    assert ffprobe_bin("ffmpeg") == "ffprobe"
    assert ffprobe_bin(r"C:\Tools\ffmpeg.exe") == r"C:\Tools\ffprobe.exe"
    assert ffprobe_bin("/usr/bin/ffmpeg").endswith("/ffprobe")


def test_copy_arguments(tmp_path: Path):
    cmd = part_command(
        ffmpeg="/bin/ffmpeg",
        source=Path("/v/in.mp4"),
        dest=Path("/v/out.mp4"),
        start=1.5,
        end=3,
    )
    assert cmd[:4] == ["/bin/ffmpeg", "-hide_banner", "-loglevel", "error"]
    assert cmd[cmd.index("-c") + 1] == "copy"
    assert cmd[cmd.index("-ss") + 1] == "1.500000"
    assert cmd[cmd.index("-to") + 1] == "3.000000"
    assert "-i" in cmd


def test_stand_in_writes_part(tmp_path: Path):
    ffmpeg = write_stub(tmp_path)
    log = tmp_path / "log"
    os.environ["VIDEOSPLITTER_STUB_LOG"] = str(log)
    os.environ["VIDEOSPLITTER_STUB_DURATION"] = "4"
    os.environ.pop("VIDEOSPLITTER_STUB_FAIL", None)
    source = tmp_path / "in.mp4"
    source.write_bytes(b"video")
    assert probe_duration(ffprobe_bin(str(ffmpeg)), source) == 4
    dest = tmp_path / "out" / "part.mp4"
    assert write_part(
        ffmpeg=str(ffmpeg),
        source=source,
        dest=dest,
        start=0,
        end=2,
        temp_dir=tmp_path,
        replace=False,
    ) == "wrote"
    assert dest.read_bytes() == b"ok"
    assert str(ffmpeg) in log.read_text(encoding="utf-8")
    assert write_part(
        ffmpeg=str(ffmpeg),
        source=source,
        dest=dest,
        start=0,
        end=2,
        temp_dir=tmp_path,
        replace=False,
    ) == "kept"
