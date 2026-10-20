# Профиль YAML

Файл: `profiles/<имя>.yml`. Новое имя → slug через translited с `-`.

## Профиль default при первом создании

- mode `size`, 1800 МБ; fixed 10 мин; flex 8–15; parts 5; min_part_minutes 8
- шаблон `{video_name|translited}_{part}.{ext}`
- кадры выкл.; время `random frame of the part`; подпись с `[is_last]…[else]…[/is_last]`

## Режимы

| Режим | Смысл |
| --- | --- |
| size | По размеру (равные по времени части) |
| fixed | Фиксированные минуты (остаток в последней) |
| flexible | Случайные длины в min…max (`VIDEOSPLITTER_FLEX_SEED`) |
| parts | N равных по времени частей |

## Шаблоны

Метки: `{video_name}`, `{file_name}`, `{ext}`, `{part}`, `{parts}`, `{source_path}`.

Блоки: `[is_last]` / `[is_first]` с необязательным `[else]`. Старый `[is_final]` не поддерживается.

Функции: `translited`, `uppercase`, `lowercase`, `capitalize`, `pad`, `int`, `round`.
