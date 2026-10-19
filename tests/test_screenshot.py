from pathlib import Path

import pytest

from videosplitter.ffmpeg import drawtext, font_file, screenshot_instant
from videosplitter.planner import Profile


def profile(**kwargs):
    base = dict(
        mode="size", size_mb=1800, minutes=30, flex_min=5, flex_max=10, parts=2,
        min_part_minutes=1, name_template="{video_name}.{ext}",
        create_screenshot=True, screenshot_time="50% of the part",
        screenshot_name="{video_name}_p{part|pad(2)}", screenshot_format="jpg",
        write_label=True, label_template="{part},[is_final][/is_final],{file_name}",
        label_font="Times New Roman", label_size_px=13, label_color="white",
        label_position=(("bottom", 15), ("right", 5)), label_border_px=2,
        label_border_color="black",
    )
    base.update(kwargs)
    return Profile(**base)


def test_part_halfway_and_video_first_and_seeded_random():
    assert screenshot_instant("50% of the part", part_start=10, part_end=20, video_end=90, random_at=None) == 15
    assert screenshot_instant("first frame of the video", part_start=10, part_end=20, video_end=90, random_at=None) == 0
    assert screenshot_instant("random frame of the part", part_start=10, part_end=20, video_end=90, random_at=12.5) == 12.5
    assert screenshot_instant("100% of the video", part_start=0, part_end=1, video_end=90, random_at=None) == 90
    assert screenshot_instant("0% of the part", part_start=10, part_end=20, video_end=90, random_at=None) == 10


def test_percent_out_of_range():
    with pytest.raises(ValueError):
        screenshot_instant("101% of the part", part_start=0, part_end=1, video_end=1, random_at=None)


def test_plain_frame_has_no_drawtext():
    from videosplitter.ffmpeg import screenshot_command

    cmd = screenshot_command(
        ffmpeg="ffmpeg", source=Path("a.mp4"), dest=Path("a.jpg"), instant=2.5, vf=None,
    )
    assert "-vf" not in cmd
    assert cmd[cmd.index("-ss") + 1] == "2.500000"


def test_label_and_plain_font(tmp_path: Path):
    font = tmp_path / "font.ttf"
    font.write_bytes(b"font")
    sample = profile(label_font=str(font))
    labeled = drawtext("1,,Holiday", sample, str(font))
    assert labeled.startswith("drawtext=")
    assert "fontsize=13" in labeled
    assert "fontcolor=white" in labeled
    assert "borderw=2" in labeled
    assert "bordercolor=black" in labeled
    assert "y=h-th-15" in labeled
    assert "x=w-tw-5" in labeled
    assert font_file(str(font)) == str(font)
    with pytest.raises(Exception, match="font not found"):
        font_file(str(tmp_path / "missing.ttf"))
