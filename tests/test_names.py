import pytest

from videosplitter.names import NameError, render


def test_tags_and_functions():
    assert render(
        "{video_name|translited|uppercase}_p{part|pad(2)}.{ext}",
        video_name="Ёж",
        ext="mp4",
        part=1,
        parts=2,
        is_final=False,
    ) == "YOZH_p01.mp4"
    assert render("{part|int}", video_name="a", ext="mp4", part=1, parts=1, is_final=True) == "1"
    assert render("{part|round(2)}", video_name="a", ext="mp4", part=1, parts=1, is_final=True) == "1.00"
    assert render("{video_name|lowercase}", video_name="Ab", ext="mp4", part=1, parts=1, is_final=True) == "ab"
    assert render("{parts}", video_name="a", ext="mp4", part=1, parts=4, is_final=False) == "4"
    assert render("{file_name}", video_name="Holiday", ext="mp4", part=1, parts=1, is_final=True) == "Holiday"


def test_is_final_block():
    template = "{part},[is_final]end[/is_final],{file_name}"
    common = dict(video_name="Holiday", ext="mp4", parts=2)
    assert render(template, part=1, is_final=False, **common) == "1,,Holiday"
    assert render(template, part=2, is_final=True, **common) == "2,end,Holiday"


def test_unknown_tag():
    with pytest.raises(NameError):
        render("{nope}", video_name="a", ext="mp4", part=1, parts=1, is_final=True)
