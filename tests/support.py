"""Stand-in ffmpeg and ffprobe. Unix shebang; Windows .cmd wrappers."""

from __future__ import annotations

import os
import stat
from pathlib import Path

_BODY = "\n".join(
    [
        "import os, pathlib, sys",
        'log = pathlib.Path(os.environ["VIDEOSPLITTER_STUB_LOG"])',
        'line = " ".join(sys.argv)',
        'prev = log.read_text(encoding="utf-8") if log.exists() else ""',
        'log.write_text(prev + line + "\\n", encoding="utf-8")',
        'if os.environ.get("VIDEOSPLITTER_STUB_FAIL"):',
        "    raise SystemExit(1)",
        'if os.environ.get("VIDEOSPLITTER_STUB_FAIL_FRAMES") and "-frames:v" in sys.argv:',
        "    raise SystemExit(1)",
        'if "-c" in sys.argv or "-frames:v" in sys.argv:',
        "    dest = pathlib.Path(sys.argv[-1])",
        "    dest.parent.mkdir(parents=True, exist_ok=True)",
        '    dest.write_bytes(b"ok")',
        'duration = os.environ.get("VIDEOSPLITTER_STUB_DURATION", "")',
        "if duration:",
        "    print(duration)",
        "",
    ]
)


def write_stub(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        script = directory / "stub.py"
        script.write_text(_BODY, encoding="utf-8")
        ffmpeg = directory / "ffmpeg.cmd"
        probe = directory / "ffprobe.cmd"
        wrapper = f'@echo off\r\npy -3 "{script}" %*\r\n'
        ffmpeg.write_text(wrapper, encoding="utf-8")
        probe.write_text(wrapper, encoding="utf-8")
        return ffmpeg
    ffmpeg = directory / "ffmpeg"
    probe = directory / "ffprobe"
    text = "#!/usr/bin/env python3\n" + _BODY
    ffmpeg.write_text(text, encoding="utf-8")
    probe.write_text(text, encoding="utf-8")
    ffmpeg.chmod(ffmpeg.stat().st_mode | stat.S_IEXEC)
    probe.chmod(probe.stat().st_mode | stat.S_IEXEC)
    return ffmpeg
