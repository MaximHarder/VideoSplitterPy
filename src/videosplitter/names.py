"""Name templates. translited maps Cyrillic to Latin; optional space replacement."""

from __future__ import annotations

import re

_RU = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}
_TAG = re.compile(r"\{([^{}]+)\}")
_BLOCK = re.compile(
    r"\[(is_last|is_first)\](.*?)(?:\[else\](.*?))?\[/\1\]",
    re.DOTALL,
)


class NameError(Exception):
    pass


def translited(text: str, space: str | bool = "-") -> str:
    out = []
    for ch in text:
        rep = _RU.get(ch.lower())
        if rep is None:
            out.append(ch)
        elif ch.isupper() and rep:
            out.append(rep[0].upper() + rep[1:])
        else:
            out.append(rep)
    result = "".join(out)
    if space is False:
        return result
    sep = "-" if space is True or space == "" else str(space)
    return re.sub(r"\s+", sep, result)


def _fn(spec: str, value: object) -> object:
    if spec == "uppercase":
        return str(value).upper()
    if spec == "lowercase":
        return str(value).lower()
    if spec == "capitalize":
        return str(value).title()
    if spec == "translited":
        return translited(str(value), space="-")
    tr = re.fullmatch(r"translited\((.*)\)", spec)
    if tr:
        raw = tr.group(1).strip()
        if raw.lower() == "false":
            return translited(str(value), space=False)
        return translited(str(value), space=raw.strip("'\""))
    if spec == "int":
        return int(float(value))
    pad = re.fullmatch(r"pad\((\d+)\)", spec)
    if pad:
        return f"{int(value):0{int(pad.group(1))}d}"
    rnd = re.fullmatch(r"round\((\d+)\)", spec)
    if rnd:
        return f"{float(value):.{int(rnd.group(1))}f}"
    raise NameError(spec)


def _tag(body: str, values: dict[str, object]) -> str:
    name, _, rest = body.partition("|")
    if name not in values:
        raise NameError(name)
    value: object = values[name]
    if rest:
        for spec in rest.split("|"):
            try:
                value = _fn(spec, value)
            except (NameError, TypeError, ValueError):
                raise NameError(spec) from None
    return str(value)


def render(
    template: str,
    *,
    video_name: str,
    ext: str,
    part: int,
    parts: int,
    is_final: bool,
    source_path: str = "",
    is_first: bool | None = None,
) -> str:
    first = part == 1 if is_first is None else is_first

    def block(match: re.Match[str]) -> str:
        kind, when_true, when_false = match.group(1), match.group(2), match.group(3)
        active = is_final if kind == "is_last" else first
        if active:
            return when_true
        return when_false if when_false is not None else ""

    text = _BLOCK.sub(block, template)
    values = {
        "video_name": video_name,
        "file_name": video_name,
        "ext": ext,
        "part": part,
        "parts": parts,
        "source_path": source_path,
    }
    return _TAG.sub(lambda match: _tag(match.group(1), values), text)


def validate_template(template: str) -> None:
    render(template, video_name="x", ext="mp4", part=1, parts=2, is_final=False, source_path="/tmp")
    render(template, video_name="x", ext="mp4", part=2, parts=2, is_final=True, source_path="/tmp")
