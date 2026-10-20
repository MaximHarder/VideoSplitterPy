from pathlib import Path

import pytest

from videosplitter.ffmpeg import draw_label, font_file, screenshot_instant
from videosplitter.planner import Profile


def profile(**kwargs):
    base = dict(
        mode="size", size_mb=1800, minutes=30, flex_min=5, flex_max=10, parts=2,
        min_part_minutes=1, name_template="{video_name}.{ext}",
        create_screenshot=True, screenshot_time="50% of the part",
        screenshot_name="{video_name}_p{part|pad(2)}", screenshot_format="jpg",
        write_label=True, label_template="[is_last]Final[else]PART {part}[/is_last]",
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


def test_plain_frame_scales_to_display_and_has_no_drawtext():
    from videosplitter.ffmpeg import screenshot_command

    cmd = screenshot_command(
        ffmpeg="ffmpeg", source=Path("a.mp4"), dest=Path("a.jpg"), instant=2.5, vf=None,
    )
    vf = cmd[cmd.index("-vf") + 1]
    assert vf == "scale=iw*sar:ih,setsar=1"
    assert "drawtext" not in vf
    assert cmd[cmd.index("-ss") + 1] == "2.500000"


def test_label_and_plain_font(tmp_path: Path):
    from PIL import Image

    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    sample = profile(label_font=font, label_color="black", label_border_px=0, label_position=(("top", 4), ("left", 4)))
    dest = tmp_path / "shot.png"
    Image.new("RGB", (200, 80), "white").save(dest)
    before = dest.read_bytes()
    draw_label(dest, "PART 1", sample, font)
    assert dest.read_bytes() != before
    fake = tmp_path / "font.ttf"
    fake.write_bytes(b"font")
    assert font_file(str(fake)) == str(fake)
    assert Path(font_file("DejaVu Sans")).is_file()
    from videosplitter.ffmpeg import system_fonts
    assert "DejaVu Sans" in system_fonts()
    with pytest.raises(Exception, match="font not found"):
        font_file(str(tmp_path / "missing.ttf"))
