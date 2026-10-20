# Split one file

## Goal

Cut one video into parts using a profile or one-off flags.

## Steps

1. Install or use `uv run` (see [First run](../tutorials/first-run.md)).
2. Run with `-f`:

```text
videosplitter -f movie.mp4
```

3. Optional: pick a profile, output folder, or split override:

```text
videosplitter -f movie.mp4 -p telegram
videosplitter -f movie.mp4 -o D:\\out
videosplitter -f movie.mp4 --split-by size --split-size 100
videosplitter -f movie.mp4 --split-by fixed --split-minutes 10
videosplitter -f movie.mp4 --split-by flexible --min-length 5 --max-length 10
videosplitter -f movie.mp4 --split-by parts --split-parts 4
```

Flags change the profile for that run only. They do not rewrite YAML.

## Notes

- If the path is a directory, you must pass `--bulk` (see [folder bulk](split-folder-bulk.md)).
- Full flag list: [CLI reference](../reference/cli.md).
