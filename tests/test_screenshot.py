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
        label_position=(("bottom", "15"), ("right", "5")), label_border_px=2,
        label_border_color="black",
        label_bg=False, label_bg_shape="parallelogram", label_bg_color="white",
        label_bg_padding_x="8", label_bg_padding_y="8", label_bg_skew_px=12,
        label_bg_border_px=2, label_bg_border_color="black",
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
    sample = profile(label_font=font, label_color="black", label_border_px=0, label_position=(("top", "4"), ("left", "4")))
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


def test_label_bg_fill_pixel(tmp_path: Path):
    from PIL import Image

    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    dest = tmp_path / "bg.png"
    Image.new("RGB", (200, 100), "black").save(dest)
    sample = profile(
        label_font=font, label_color="black", label_border_px=0,
        label_position=(("top", "10"), ("left", "10")),
        label_bg=True, label_bg_shape="rect", label_bg_color="red",
        label_bg_padding_x="20", label_bg_padding_y="10",
        label_bg_border_px=0, label_bg_skew_px=0,
    )
    draw_label(dest, "X", sample, font)
    pix = Image.open(dest).load()
    # Far corner of padding (away from glyph AA) is fill color.
    assert pix[2, 2] == (255, 0, 0)


def test_label_center_on_percent(tmp_path: Path):
    from PIL import Image

    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    dest = tmp_path / "mid.png"
    Image.new("RGB", (200, 100), "white").save(dest)
    sample = profile(
        label_font=font, label_color="black", label_border_px=0,
        label_position=(("top", "50%"), ("left", "50%")),
        label_bg=True, label_bg_shape="rect", label_bg_color="blue",
        label_bg_padding_x="4", label_bg_padding_y="4",
        label_bg_border_px=0, label_bg_skew_px=0,
    )
    draw_label(dest, "MID", sample, font)
    img = Image.open(dest)
    # Find blue bbox; its center should be near frame center.
    xs, ys = [], []
    pix = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if pix[x, y] == (0, 0, 255):
                xs.append(x)
                ys.append(y)
    assert xs and ys
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    assert abs(cx - 100) <= 3
    assert abs(cy - 50) <= 3


def test_label_padding_percent_scales(tmp_path: Path):
    from PIL import Image

    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    dest = tmp_path / "pad.png"
    Image.new("RGB", (200, 100), "black").save(dest)
    sample = profile(
        label_font=font, label_color="white", label_border_px=0,
        label_position=(("top", "50%"), ("left", "50%")),
        label_bg=True, label_bg_shape="rect", label_bg_color="green",
        label_bg_padding_x="10%", label_bg_padding_y="10%",
        label_bg_border_px=0, label_bg_skew_px=0,
    )
    draw_label(dest, "P", sample, font)
    img = Image.open(dest)
    pix = img.load()
    greens = [
        (x, y) for y in range(img.height) for x in range(img.width)
        if pix[x, y][1] >= 100 and pix[x, y][0] < 40 and pix[x, y][2] < 40
    ]
    assert greens
    width = max(x for x, _ in greens) - min(x for x, _ in greens) + 1
    # 10% of 200 = 20px pad each side → bg at least ~40px wider than bare glyph
    assert width >= 40
