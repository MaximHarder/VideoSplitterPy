# CLI flags

Flags override the profile for that run. They are not saved.

```text
videosplitter -f movie.mp4
videosplitter -f ./videos --bulk
videosplitter -f ./videos --bulk --subfolders
videosplitter -f movie.mp4 -o D:\\out
videosplitter -f movie.mp4 -p telegram
videosplitter -f movie.mp4 -p telegram --split-by size --split-size 100
videosplitter -f movie.mp4 --split-by fixed --split-minutes 10
videosplitter -f movie.mp4 --split-by flexible --min-length 5 --max-length 10
videosplitter -f movie.mp4 --split-by parts --split-parts 4
```

| Flag | Meaning |
| --- | --- |
| `-f` | One file, or a folder when you also pass `--bulk` |
| `--bulk` | The source is a folder. Required for a folder. Error if `-f` is a file |
| `--subfolders`, `-sf` | With `--bulk` only. Also search child folders, and rebuild that relative path under the output folder |
| `-o` | Output folder for this run |
| `-p` | Profile name. Wins over `default_profile` |
| `--split-by` | `size`, `fixed`, `flexible`, or `parts` |
| `--split-size` | MB, for `size` |
| `--split-minutes` | Minutes in one part, for `fixed` |
| `--min-length`, `--max-length` | Minutes, for `flexible` |
| `--split-parts` | How many parts, for `parts`. Minimum 1 |

No `-f` starts the [wizard](wizard.md).

There is no CLI flag for the config folder. Use the environment variable `VIDEOSPLITTER_CONFIG` to point at another folder (path to the folder that contains `settings.yml`).
