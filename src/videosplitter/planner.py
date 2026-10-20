"""Pure split planner. Empty list means do not split."""

from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Part:
    index: int
    start: float
    end: float


@dataclass(frozen=True)
class Profile:
    mode: str
    size_mb: float
    minutes: float
    flex_min: float
    flex_max: float
    parts: int
    min_part_minutes: float
    name_template: str
    create_screenshot: bool
    screenshot_time: str
    screenshot_name: str
    screenshot_format: str
    write_label: bool
    label_template: str
    label_font: str
    label_size_px: int
    label_color: str
    label_position: tuple[tuple[str, int], ...]
    label_border_px: int
    label_border_color: str


class PlanError(Exception):
    pass


def _equal(duration: float, count: int) -> list[Part]:
    parts = []
    for i in range(count):
        start = duration * i / count
        end = duration if i == count - 1 else duration * (i + 1) / count
        parts.append(Part(i + 1, start, end))
    return parts


def _flex_rng(rng: random.Random | None) -> random.Random:
    if rng is not None:
        return rng
    seed = os.environ.get("VIDEOSPLITTER_FLEX_SEED")
    if seed is not None and seed != "":
        return random.Random(int(seed))
    return random.Random()


def _flexible_random(duration_s: float, min_s: float, max_s: float, rng: random.Random) -> list[Part]:
    if duration_s <= max_s:
        return []
    parts: list[Part] = []
    start = 0.0
    index = 1
    for _ in range(10_000):
        remaining = duration_s - start
        if remaining <= 0:
            break
        if remaining <= max_s and remaining >= min_s:
            parts.append(Part(index, start, duration_s))
            return parts
        if remaining < min_s:
            raise PlanError("flexible bounds")
        room_for_next = remaining - min_s
        upper = min(max_s, room_for_next)
        if upper < min_s:
            if remaining > max_s:
                raise PlanError("flexible bounds")
            parts.append(Part(index, start, duration_s))
            return parts
        length = rng.uniform(min_s, upper)
        end = start + length
        parts.append(Part(index, start, end))
        start = end
        index += 1
    raise PlanError("flexible bounds")


def plan(
    profile: Profile,
    duration_s: float,
    size_bytes: int,
    *,
    rng: random.Random | None = None,
) -> list[Part]:
    if duration_s < profile.min_part_minutes * 60:
        return []
    if profile.mode == "size":
        limit = profile.size_mb * 1024 * 1024
        count = math.ceil(size_bytes / limit) if limit > 0 else 1
        if count <= 1:
            return []
        return _equal(duration_s, count)
    if profile.mode == "fixed":
        slice_s = profile.minutes * 60
        if duration_s <= slice_s:
            return []
        parts = []
        start = 0.0
        index = 1
        while start < duration_s:
            end = min(duration_s, start + slice_s)
            parts.append(Part(index, start, end))
            start = end
            index += 1
        return parts
    if profile.mode == "flexible":
        min_s = profile.flex_min * 60
        max_s = profile.flex_max * 60
        return _flexible_random(duration_s, min_s, max_s, _flex_rng(rng))
    if profile.parts < 2:
        return []
    return _equal(duration_s, profile.parts)
