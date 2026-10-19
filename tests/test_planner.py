import pytest

from videosplitter.planner import PlanError, Profile, plan


def profile(**kwargs):
    base = dict(
        mode="size",
        size_mb=1800,
        minutes=30,
        flex_min=5,
        flex_max=10,
        parts=2,
        min_part_minutes=1,
        name_template="{video_name}_p{part|pad(2)}.{ext}",
        create_screenshot=False,
        screenshot_time="50% of the part",
        screenshot_name="{video_name}_p{part|pad(2)}",
        screenshot_format="jpg",
        write_label=False,
        label_template="{part},[is_final][/is_final],{file_name}",
        label_font="Times New Roman",
        label_size_px=13,
        label_color="white",
        label_position=(("bottom", 15), ("right", 5)),
        label_border_px=2,
        label_border_color="black",
    )
    base.update(kwargs)
    return Profile(**base)


def test_skip_under_one_minute():
    assert plan(profile(), 40, 9_000_000_000) == []


def test_size_two_equal_parts():
    duration = 100.0
    nbytes = 3000 * 1024 * 1024
    parts = plan(profile(size_mb=1800), duration, nbytes)
    assert len(parts) == 2
    assert parts[0].start == 0
    assert parts[0].end == pytest.approx(50)
    assert parts[1].end == duration


def test_size_already_under_limit():
    assert plan(profile(size_mb=1800), 600, 1000) == []


def test_fixed_remainder():
    parts = plan(profile(mode="fixed", minutes=30), 50 * 60, 1)
    assert len(parts) == 2
    assert parts[0].end == pytest.approx(30 * 60)
    assert parts[1].end == pytest.approx(50 * 60)
    assert (parts[1].end - parts[1].start) == pytest.approx(20 * 60)


def test_fixed_fits_one_slice():
    assert plan(profile(mode="fixed", minutes=30), 30 * 60, 1) == []


def test_flexible_equal():
    parts = plan(profile(mode="flexible", flex_min=5, flex_max=10), 23 * 60, 1)
    assert len(parts) == 3
    assert parts[0].end - parts[0].start == pytest.approx(23 * 60 / 3)
    assert parts[2].end == pytest.approx(23 * 60)


def test_flexible_impossible():
    with pytest.raises(PlanError, match="flexible bounds"):
        plan(profile(mode="flexible", flex_min=8, flex_max=10), 11 * 60, 1)


def test_flexible_under_max_is_not_split():
    assert plan(profile(mode="flexible", flex_min=5, flex_max=10), 10 * 60, 1) == []


def test_parts():
    parts = plan(profile(mode="parts", parts=4), 40 * 60, 1)
    assert [p.index for p in parts] == [1, 2, 3, 4]
    assert parts[-1].end == pytest.approx(40 * 60)


def test_parts_one_does_not_split():
    assert plan(profile(mode="parts", parts=1), 600, 1) == []


def test_exact_minimum_still_splits():
    parts = plan(profile(mode="parts", parts=2, min_part_minutes=1), 60, 1)
    assert len(parts) == 2
