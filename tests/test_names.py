import pytest

from videosplitter.names import NameError, render


def test_tags_and_functions():
    assert render(
        "{video_name|translited|uppercase}_{part|pad(2)}.{ext}",
        video_name="Ёж",
        ext="mp4",
        part=1,
        parts=2,
        is_final=False,
    ) == "YOZH_01.mp4"
    assert render("{part|int}", video_name="a", ext="mp4", part=1, parts=1, is_final=True) == "1"
    assert render("{part|round(2)}", video_name="a", ext="mp4", part=1, parts=1, is_final=True) == "1.00"
    assert render("{video_name|lowercase}", video_name="Ab", ext="mp4", part=1, parts=1, is_final=True) == "ab"
    assert render("{video_name|capitalize}", video_name="hello world", ext="mp4", part=1, parts=1, is_final=True) == "Hello World"
    assert render("{parts}", video_name="a", ext="mp4", part=1, parts=4, is_final=False) == "4"
    assert render("{file_name}", video_name="Holiday", ext="mp4", part=1, parts=1, is_final=True) == "Holiday"
    assert render("{source_path}", video_name="a", ext="mp4", part=1, parts=1, is_final=True, source_path="/data") == "/data"
    assert render("{video_name|translited}", video_name="a b", ext="mp4", part=1, parts=1, is_final=True) == "a-b"
    assert render("{video_name|translited(false)}", video_name="a b", ext="mp4", part=1, parts=1, is_final=True) == "a b"


def test_is_last_else_block():
    template = "[is_last]Final[else]PART {part|uppercase}[/is_last]"
    common = dict(video_name="Holiday", ext="mp4", parts=2)
    assert render(template, part=1, is_final=False, **common) == "PART 1"
    assert render(template, part=2, is_final=True, **common) == "Final"


def test_is_first_block():
    template = "[is_first]first[else]later[/is_first]"
    common = dict(video_name="a", ext="mp4", parts=2)
    assert render(template, part=1, is_final=False, **common) == "first"
    assert render(template, part=2, is_final=True, **common) == "later"


def test_unknown_tag():
    with pytest.raises(NameError):
        render("{nope}", video_name="a", ext="mp4", part=1, parts=1, is_final=True)
