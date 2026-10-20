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
    # Do not inherit the text UI's streams: their fileno() is -1.
    return subprocess.run(
        cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
    )


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


def _fc_match(name: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["fc-match", "-f", "%{family}\n%{file}", name],
            text=True, stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    family, _, file = out.strip().partition("\n")
    if name.casefold() not in family.casefold():
        return None
    path = Path(file.strip())
    return str(path) if path.is_file() else None


def system_fonts() -> tuple[str, ...]:
    try:
        out = subprocess.check_output(
            ["fc-list", "-f", "%{family}\n"],
            text=True, stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return ()
    names = {line.split(",", 1)[0].strip() for line in out.splitlines()}
    names.discard("")
    return tuple(sorted(names, key=str.casefold))


def font_file(label_font: str) -> str:
    candidate = Path(label_font)
    if candidate.is_file():
        return str(candidate)
    if label_font == "Times New Roman":
        for path in _TIMES:
            if path.is_file():
                return str(path)
    found = _fc_match(label_font)
    if found is not None:
        return found
    raise FfmpegError("font not found")


def draw_label(dest: Path, text: str, profile: Profile, fontfile: str) -> None:
    from PIL import Image, ImageDraw, ImageFont

    pos = dict(profile.label_position)
    vertical = "bottom" if "bottom" in pos else "top"
    horizontal = "right" if "right" in pos else "left"
    anchor = {("top", "left"): "lt", ("top", "right"): "rt", ("bottom", "left"): "lb", ("bottom", "right"): "rb"}[(vertical, horizontal)]
    with Image.open(dest) as img:
        x = pos.get("left", 0) if horizontal == "left" else img.width - pos.get("right", 0)
        y = pos.get("top", 0) if vertical == "top" else img.height - pos.get("bottom", 0)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(fontfile, profile.label_size_px)
        draw.text(
            (x, y), text, font=font, fill=profile.label_color, anchor=anchor,
            stroke_width=profile.label_border_px, stroke_fill=profile.label_border_color,
        )
        img.save(dest)


# Square pixels at the size a player shows. Raw 1920x1080 with a tall ratio stays wide otherwise.
_DISPLAY_SCALE = "scale=iw*sar:ih,setsar=1"


def screenshot_command(*, ffmpeg: str, source: Path, dest: Path, instant: float, vf: str | None) -> list[str]:
    graph = _DISPLAY_SCALE if vf is None else f"{_DISPLAY_SCALE},{vf}"
    return [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-ss", _seconds(instant), "-i", str(source), "-frames:v", "1",
        "-vf", graph, str(dest),
    ]


def write_screenshot(*, ffmpeg: str, source: Path, dest: Path, instant: float, vf: str | None, replace: bool) -> None:
    if dest.exists() and not replace:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Keep the image suffix: ffmpeg refuses *.jpg.tmp.
    tmp = dest.with_name(f".{dest.stem}.part{dest.suffix}")
    result = popen(screenshot_command(ffmpeg=ffmpeg, source=source, dest=tmp, instant=instant, vf=vf))
    if result.returncode != 0 or not tmp.is_file():
        tmp.unlink(missing_ok=True)
        raise FfmpegError("screenshot failed")
    os.replace(tmp, dest)
