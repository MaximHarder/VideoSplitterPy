"""Pure split planner. Empty list means do not split."""

from __future__ import annotations

import math
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


def plan(profile: Profile, duration_s: float, size_bytes: int) -> list[Part]:
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
        max_s = profile.flex_max * 60
        if duration_s <= max_s:
            return []
        count = math.ceil(duration_s / max_s)
        if duration_s / count < profile.flex_min * 60:
            raise PlanError("flexible bounds")
        return _equal(duration_s, count)
    if profile.parts < 2:
        return []
    return _equal(duration_s, profile.parts)
