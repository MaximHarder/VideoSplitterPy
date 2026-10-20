# How splitting works

## Big picture

1. Load settings (create defaults on first run).
2. Load the profile (`-p` or `default_profile`), then apply `--split-by` overrides.
3. Collect files: one `-f` file, or a folder for `--bulk`, plus children when `-sf` is set. Skip extensions not in the list.
4. For each video: length from `ffprobe`, size from the file.
5. The **planner** returns time ranges, or “do not split”. The planner does not call FFmpeg.
6. If there is no split, leave the file on disk.
7. For each part: build the name, write with `ffmpeg -c copy` in the temp folder, move to the output folder. **Stream copy** means a cut, not a new encode.
8. If replace is off and the output name exists, keep the old file (not a failure).
9. If a part fails: stop that video, delete the temp file, do not delete the source.
10. If every part succeeded and at least one new file was written, delete the source only when remove-source is on.
11. Screenshots (if on) are written after the part file is in place; a screenshot failure fails that video.

## When it will not split

- Video shorter than the minimum part length (default 1 minute)
- Size mode and the file already fits the limit
- Fixed time and the video fits in one slice
- Flexible time and the video fits under the maximum
- Parts mode with one part requested
- Extension not in the settings list (ignored in a folder)

Flexible time can also **error** when min and max cannot both be met — that is a failure, not a silent skip.

## Words

| Word | Meaning |
| --- | --- |
| Profile | YAML with one split rule, name template, screenshot choices |
| Part | One time range cut from the source |
| Planner | Decides time ranges; does not call FFmpeg |
| Stream copy | FFmpeg `-c copy`: cut without re-encoding |
| Bulk | Split every matching video in a folder |
| `{source_dir}` | Source folder used in the output path |
