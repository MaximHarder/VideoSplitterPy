"""Flags, wizard, and the per-video run."""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, replace
from pathlib import Path

from cyclopts import App, Parameter
from typing import Annotated

from videosplitter import __version__
from videosplitter.ffmpeg import (
    FfmpegError,
    drawtext,
    ffprobe_bin,
    font_file,
    probe_duration,
    screenshot_instant,
    validate_screenshot_time,
    write_part,
    write_screenshot,
)
from videosplitter.names import NameError, render, validate_template
from videosplitter.planner import PlanError, Profile, plan
from videosplitter.store import ConfigError, ensure, load_profile, load_settings, temp_path

app = App(name="videosplitter", version=__version__, help="Split a video into parts.")


@dataclass(frozen=True)
class Request:
    path: Path | None
    bulk: bool
    subfolders: bool
    output: str | None
    profile_name: str | None
    split_by: str | None
    split_size: float | None
    split_minutes: float | None
    min_length: float | None
    max_length: float | None
    split_parts: int | None


class UsageError(Exception):
    pass


class AnswerError(Exception):
    pass


def apply_override(profile: Profile, request: Request) -> Profile:
    mode = request.split_by
    if mode is None:
        return profile
    if mode == "size":
        if request.split_size is None or request.split_size <= 0:
            raise UsageError("incomplete split override")
        return replace(profile, mode="size", size_mb=request.split_size)
    if mode == "fixed":
        if request.split_minutes is None or request.split_minutes <= 0:
            raise UsageError("incomplete split override")
        return replace(profile, mode="fixed", minutes=request.split_minutes)
    if mode == "flexible":
        if request.min_length is None or request.max_length is None or request.min_length <= 0 or request.max_length <= 0:
            raise UsageError("incomplete split override")
        if request.min_length > request.max_length:
            raise UsageError("flexible minimum is greater than maximum")
        return replace(profile, mode="flexible", flex_min=request.min_length, flex_max=request.max_length)
    if mode == "parts":
        if request.split_parts is None or request.split_parts < 1:
            raise UsageError("incomplete split override")
        return replace(profile, mode="parts", parts=request.split_parts)
    raise UsageError("incomplete split override")


def _validate(profile: Profile) -> None:
    try:
        validate_template(profile.name_template)
        if profile.write_label:
            validate_template(profile.label_template)
        if profile.create_screenshot:
            validate_template(profile.screenshot_name)
    except NameError:
        raise UsageError("unknown template") from None
    if not profile.create_screenshot:
        return
    try:
        validate_screenshot_time(profile.screenshot_time)
    except ValueError:
        if re.fullmatch(r"-?\d+% of the (part|video)", profile.screenshot_time.strip()):
            raise UsageError("screenshot percent out of range") from None
        raise UsageError("unknown screenshot time") from None


def collect(path: Path, *, bulk: bool, subfolders: bool, extensions: tuple[str, ...]) -> list[Path]:
    if not bulk:
        return [path]
    allowed = {item.lower().lstrip(".") for item in extensions}
    pattern = "**/*" if subfolders else "*"
    return sorted(
        item for item in path.glob(pattern)
        if item.is_file() and item.suffix.lower().lstrip(".") in allowed
    )


def _output_dir(file: Path, request: Request, output_dir: str) -> Path:
    if request.output:
        base = Path(request.output)
    else:
        token = str(request.path if request.bulk else file.parent)
        base = Path(output_dir.replace("{source_dir}", token))
    if request.bulk and request.subfolders and request.path is not None:
        return base / file.parent.relative_to(request.path)
    return base


def execute(request: Request, *, config: Path | None = None, random_at: float | None = None) -> int:
    if config is None and os.environ.get("VIDEOSPLITTER_CONFIG"):
        config = Path(os.environ["VIDEOSPLITTER_CONFIG"])
    try:
        root = ensure(config)
        settings = load_settings(root)
        profile = apply_override(load_profile(root, request.profile_name or settings.default_profile), request)
        _validate(profile)
    except (UsageError, ConfigError) as exc:
        print(exc, file=sys.stderr)
        return 2
    path = request.path
    if path is None or not path.exists():
        print("path not found", file=sys.stderr)
        return 2
    if path.is_dir() and not request.bulk:
        print("directory requires --bulk", file=sys.stderr)
        return 2
    if request.bulk and not path.is_dir():
        print("--bulk requires a directory", file=sys.stderr)
        return 2
    if request.subfolders and not request.bulk:
        print("--subfolders requires --bulk", file=sys.stderr)
        return 2
    files = collect(path, bulk=request.bulk, subfolders=request.subfolders, extensions=settings.extensions)
    if request.bulk and not files:
        print("no videos")
        return 0
    failed = False
    for file in files:
        if not _one(file, request, settings, profile, random_at):
            failed = True
    return 1 if failed else 0


def _one(file: Path, request: Request, settings, profile: Profile, random_at: float | None) -> bool:
    try:
        duration = probe_duration(ffprobe_bin(settings.ffmpeg), file)
        parts = plan(profile, duration, file.stat().st_size)
    except FfmpegError as exc:
        print(f"fail {file}: {exc}", file=sys.stderr)
        return False
    except PlanError as exc:
        print(f"fail {file}: {exc}", file=sys.stderr)
        return False
    if not parts:
        print(f"skip {file}")
        return True
    out = _output_dir(file, request, settings.output_dir)
    try:
        out.mkdir(parents=True, exist_ok=True)
    except OSError:
        print(f"fail {file}: cannot create output", file=sys.stderr)
        return False
    wrote_new = False
    for part in parts:
        final = part.index == len(parts)
        ext = file.suffix.lstrip(".")
        try:
            part_name = render(profile.name_template, video_name=file.stem, ext=ext, part=part.index, parts=len(parts), is_final=final)
            status = write_part(
                ffmpeg=settings.ffmpeg, source=file, dest=out / part_name,
                start=part.start, end=part.end, temp_dir=temp_path(settings), replace=settings.replace_existing,
            )
            if status == "wrote":
                wrote_new = True
            if profile.create_screenshot:
                _shot(file, out, profile, part, len(parts), duration, settings.ffmpeg, random_at, settings.replace_existing)
        except (FfmpegError, NameError) as exc:
            print(f"fail {file}: {exc}", file=sys.stderr)
            return False
    if wrote_new and settings.remove_source:
        file.unlink()
    print(f"wrote {file}")
    return True


def _shot(file, out, profile, part, count, duration, ffmpeg, random_at, replace: bool) -> None:
    if profile.screenshot_format not in {"jpg", "png", "webp"}:
        raise FfmpegError("screenshot failed")
    final = part.index == count
    ext = file.suffix.lstrip(".")
    stem = render(profile.screenshot_name, video_name=file.stem, ext=ext, part=part.index, parts=count, is_final=final)
    dest = out / f"{stem}.{profile.screenshot_format}"
    instant = screenshot_instant(
        profile.screenshot_time, part_start=part.start, part_end=part.end,
        video_end=duration, random_at=random_at,
    )
    vf = None
    if profile.write_label:
        text = render(profile.label_template, video_name=file.stem, ext=ext, part=part.index, parts=count, is_final=final)
        vf = drawtext(text, profile, font_file(profile.label_font))
    write_screenshot(ffmpeg=ffmpeg, source=file, dest=dest, instant=instant, vf=vf, replace=replace)


def _yn(value: str) -> bool:
    text = value.strip().lower()
    if text not in {"y", "n"}:
        raise AnswerError("invalid answer")
    return text == "y"


def _number(value: str) -> float:
    try:
        return float(value.strip())
    except ValueError:
        raise UsageError("incomplete split override") from None


def answers_to_request(lines: list[str], *, exists, is_dir) -> Request:
    cursor = iter(lines)
    raw_path = next(cursor, "")
    path = Path(raw_path)
    if not exists(path):
        raise UsageError("path not found")
    bulk = bool(is_dir(path))
    subfolders = _yn(next(cursor)) if bulk else False
    profile_name = next(cursor, "").strip() or None
    override = _yn(next(cursor))
    split_by = split_size = split_minutes = min_length = max_length = split_parts = None
    if override:
        split_by = next(cursor, "").strip()
        if split_by == "size":
            split_size = _number(next(cursor, ""))
        elif split_by == "fixed":
            split_minutes = _number(next(cursor, ""))
        elif split_by == "flexible":
            min_length = _number(next(cursor, ""))
            max_length = _number(next(cursor, ""))
        elif split_by == "parts":
            split_parts = int(_number(next(cursor, "")))
        else:
            raise UsageError("incomplete split override")
    output = next(cursor, "").strip() or None
    return Request(
        path, bulk, subfolders, output, profile_name, split_by,
        split_size, split_minutes, min_length, max_length, split_parts,
    )


def wizard(lines: list[str] | None = None) -> int:
    if lines is None:
        print("Path: ", end="", file=sys.stderr)
        entered = sys.stdin.readline().rstrip("\n")
        path = Path(entered)
        seq = [entered]
        if path.is_dir():
            print("Include subfolders? [y/n]: ", end="", file=sys.stderr)
            seq.append(sys.stdin.readline().rstrip("\n"))
        for prompt in ("Profile name (empty for default): ", "Override split mode? [y/n]: "):
            print(prompt, end="", file=sys.stderr)
            seq.append(sys.stdin.readline().rstrip("\n"))
        if seq[-1].strip().lower() == "y":
            print("Split by [size/fixed/flexible/parts]: ", end="", file=sys.stderr)
            mode = sys.stdin.readline().rstrip("\n")
            seq.append(mode)
            prompts = {
                "size": ("MB: ",),
                "fixed": ("Minutes: ",),
                "flexible": ("Minimum minutes: ", "Maximum minutes: "),
                "parts": ("Parts: ",),
            }.get(mode.strip(), ())
            for prompt in prompts:
                print(prompt, end="", file=sys.stderr)
                seq.append(sys.stdin.readline().rstrip("\n"))
        print("Output directory (empty for settings): ", end="", file=sys.stderr)
        seq.append(sys.stdin.readline().rstrip("\n"))
        lines = seq
    try:
        request = answers_to_request(lines, exists=Path.exists, is_dir=Path.is_dir)
    except AnswerError as exc:
        print(exc, file=sys.stderr)
        return 2
    except UsageError as exc:
        print(exc, file=sys.stderr)
        return 2
    return execute(request)


def command(
    file: Annotated[str | None, Parameter(name=["--file", "-f"])] = None,
    *,
    bulk: Annotated[bool, Parameter(name="--bulk")] = False,
    subfolders: Annotated[bool, Parameter(name=["--subfolders", "-sf"])] = False,
    output: Annotated[str | None, Parameter(name=["--output", "-o"])] = None,
    profile: Annotated[str | None, Parameter(name=["--profile", "-p"])] = None,
    split_by: Annotated[str | None, Parameter(name="--split-by")] = None,
    split_size: Annotated[float | None, Parameter(name="--split-size")] = None,
    split_minutes: Annotated[float | None, Parameter(name="--split-minutes")] = None,
    min_length: Annotated[float | None, Parameter(name="--min-length")] = None,
    max_length: Annotated[float | None, Parameter(name="--max-length")] = None,
    split_parts: Annotated[int | None, Parameter(name="--split-parts")] = None,
) -> int:
    if file is None:
        return wizard()
    return execute(Request(
        Path(file), bulk, subfolders, output, profile, split_by,
        split_size, split_minutes, min_length, max_length, split_parts,
    ))


app.default(command)


def main() -> None:
    app()
