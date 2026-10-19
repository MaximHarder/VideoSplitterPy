"""ffprobe, stream copy, and screenshots."""

from __future__ import annotations

import os
import random
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from videosplitter.planner import Profile


class FfmpegError(Exception):
    pass


def ffprobe_bin(ffmpeg: str) -> str:
    pairs = (
        ("ffmpeg.exe", "ffprobe.exe"),
        ("ffmpeg.cmd", "ffprobe.cmd"),
        ("ffmpeg", "ffprobe"),
    )
    lowered = ffmpeg.lower()
    for src, dst in pairs:
        if lowered.endswith(src):
            return ffmpeg[: -len(src)] + dst
    return "ffprobe"


def popen(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def _seconds(value: float) -> str:
    return f"{value:.6f}"


def part_command(*, ffmpeg: str, source: Path, dest: Path, start: float, end: float) -> list[str]:
    return [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-ss", _seconds(start), "-to", _seconds(end),
        "-i", str(source), "-c", "copy", str(dest),
    ]


def probe_duration(ffprobe: str, source: Path) -> float:
    cmd = [
        ffprobe, "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(source),
    ]
    result = popen(cmd)
    if result.returncode != 0:
        raise FfmpegError(f"ffprobe exited {result.returncode}")
    try:
        duration = float(result.stdout.strip())
    except ValueError:
        raise FfmpegError("no duration") from None
    if duration <= 0:
        raise FfmpegError("no duration")
    return duration


def write_part(*, ffmpeg: str, source: Path, dest: Path, start: float, end: float, temp_dir: Path, replace: bool) -> str:
    if dest.exists() and not replace:
        return "kept"
    dest.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="videosplitter-", dir=temp_dir))
    tmp = work / dest.name
    try:
        result = popen(part_command(ffmpeg=ffmpeg, source=source, dest=tmp, start=start, end=end))
        if result.returncode != 0 or not tmp.is_file():
            raise FfmpegError(f"ffmpeg exited {result.returncode}")
        try:
            os.replace(tmp, dest)
        except OSError:
            if dest.exists() and replace:
                dest.unlink()
            shutil.move(str(tmp), dest)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return "wrote"


_TIMES = (
    Path(r"C:\Windows\Fonts\times.ttf"),
    Path("/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"),
    Path("/usr/share/fonts/truetype/msttcorefonts/times.ttf"),
    Path("/Library/Fonts/Times New Roman.ttf"),
    Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf"),
)
_PERCENT = re.compile(r"(-?\d+)% of the (part|video)\Z")
_PHRASES = {
    "first frame of the part": ("part", "first"),
    "last frame of the part": ("part", "last"),
    "random frame of the part": ("part", "random"),
    "first frame of the video": ("video", "first"),
    "last frame of the video": ("video", "last"),
    "random frame of the video": ("video", "random"),
}


def screenshot_instant(spec: str, *, part_start: float, part_end: float, video_end: float, random_at: float | None) -> float:
    text = spec.strip()
    match = _PERCENT.fullmatch(text)
    if match:
        percent = int(match.group(1))
        if percent < 0 or percent > 100:
            raise ValueError(spec)
        start, end = (part_start, part_end) if match.group(2) == "part" else (0.0, video_end)
        if percent == 100:
            return end
        return start + (end - start) * percent / 100
    phrase = _PHRASES.get(text)
    if phrase is None:
        raise ValueError(spec)
    span, which = phrase
    start, end = (part_start, part_end) if span == "part" else (0.0, video_end)
    if which == "first":
        return start
    if which == "last":
        return end
    if random_at is not None:
        return random_at
    if end <= start:
        return start
    return start + (end - start) * random.random()


def validate_screenshot_time(spec: str) -> None:
    screenshot_instant(spec, part_start=0, part_end=1, video_end=1, random_at=0)


def font_file(label_font: str) -> str:
    candidate = Path(label_font)
    if candidate.is_file():
        return str(candidate)
    if label_font == "Times New Roman":
        for path in _TIMES:
            if path.is_file():
                return str(path)
    raise FfmpegError("font not found")


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("%", "\\%").replace("'", "'\\''")


def drawtext(text: str, profile: Profile, fontfile: str) -> str:
    x = y = None
    for key, px in profile.label_position:
        if key == "left":
            x = str(px)
        elif key == "right":
            x = f"w-tw-{px}"
        elif key == "top":
            y = str(px)
        elif key == "bottom":
            y = f"h-th-{px}"
    bits = [
        f"text='{_escape(text)}'",
        f"fontfile='{_escape(fontfile)}'",
        f"fontsize={profile.label_size_px}",
        f"fontcolor={profile.label_color}",
        f"borderw={profile.label_border_px}",
        f"bordercolor={profile.label_border_color}",
    ]
    if x is not None:
        bits.append(f"x={x}")
    if y is not None:
        bits.append(f"y={y}")
    return "drawtext=" + ":".join(bits)


def screenshot_command(*, ffmpeg: str, source: Path, dest: Path, instant: float, vf: str | None) -> list[str]:
    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-ss", _seconds(instant), "-i", str(source), "-frames:v", "1",
    ]
    if vf is not None:
        cmd.extend(["-vf", vf])
    cmd.append(str(dest))
    return cmd


def write_screenshot(*, ffmpeg: str, source: Path, dest: Path, instant: float, vf: str | None, replace: bool) -> None:
    if dest.exists() and not replace:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    result = popen(screenshot_command(ffmpeg=ffmpeg, source=source, dest=tmp, instant=instant, vf=vf))
    if result.returncode != 0 or not tmp.is_file():
        tmp.unlink(missing_ok=True)
        raise FfmpegError("screenshot failed")
    os.replace(tmp, dest)
