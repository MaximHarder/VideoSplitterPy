# Split every video in a folder

## Goal

Process all matching videos in a folder (and optionally in child folders).

## Steps

```text
videosplitter -f ./videos --bulk
videosplitter -f ./videos --bulk --subfolders
```

- `--bulk` is required when `-f` is a directory. It is an error if `-f` is a file.
- `--subfolders` / `-sf` only works with `--bulk`. It also rebuilds the relative path under the output folder.

Example: with `--subfolders`, `videos/trip/day1/clip.mp4` is written under `output/trip/day1/`. The bulk root `videos` is not repeated in the output path.

`--bulk` without `--subfolders` reads only the folder you named, not its children.

Which extensions count as video comes from [settings](../reference/settings-yml.md).
