# Profile YAML

File: `profiles/<name>.yml`. New profile names become translited slugs with `-` (e.g. `My Profile` → `my-profile.yml`).

## Default profile (first create)

- mode `size`, size_mb `1800`
- fixed minutes `10`, flex_min `8`, flex_max `15`, parts `5`
- min_part_minutes `8`
- name_template `{video_name|translited}_{part}.{ext}`
- screenshots off; time `random frame of the part`; label uses `[is_last]…[else]…[/is_last]`
- label position `bottom: 15`, `right: 10`
- label background off by default (`label_bg: false`); shape `parallelogram`

## Label background

| Key | Meaning |
| --- | --- |
| `label_bg` | Draw a filled shape under the text |
| `label_bg_shape` | `rect` or `parallelogram` |
| `label_bg_color` / `label_bg_border_*` | Fill and outline |
| `label_bg_padding_x` / `label_bg_padding_y` | Inset around text: bare `N` = pixels, `N%` = percent of frame width/height |
| `label_bg_skew_px` | Horizontal shear for parallelogram (ignored for rect) |

Position values (`top`/`bottom`/`left`/`right`) also accept `N` or `N%` of the frame. If any position length uses `%`, the **center** of the sticker (text + padding) sits on that point (e.g. `top: 50%` + `left: 50%` = middle of the frame). Pure pixel positions keep the usual corner anchors.

## Modes

| Mode | Meaning |
| --- | --- |
| size | Parts by target file size (equal time slices) |
| fixed | Fixed minutes per part (last gets remainder) |
| flexible | Random lengths between min and max (seed: `VIDEOSPLITTER_FLEX_SEED`) |
| parts | N equal-time parts |

## Templates

Tags: `{video_name}`, `{file_name}` (alias), `{ext}`, `{part}`, `{parts}`, `{source_path}`.

Blocks: `[is_last]A[else]B[/is_last]`, `[is_first]A[else]B[/is_first]` (else optional). Old `[is_final]` is not supported.

Functions: `translited` / `translited(-)` / `translited(false)`, `uppercase`, `lowercase`, `capitalize`, `pad(n)`, `int`, `round(n)`.
