# VideoSplitterPy

Split a video into parts with FFmpeg (stream copy — no re-encode). Console command: `videosplitter`.

## Quick start

```text
uv tool install .
videosplitter -f movie.mp4
```

Or from a checkout:

```text
uv sync
uv run videosplitter -f movie.mp4
```

You need FFmpeg (`ffmpeg` / `ffprobe`) on the machine.

### Wizard (no flags)

```text
videosplitter
```

Opens a Textual menu: **Settings**, **Split-Profiles**, **Start Split** (English UI). With `-f`, the flag-based CLI runs instead.

## Docs

Full guides (English and Russian), including local development in PyCharm:

- [Documentation index](docs/README.md)

## Develop

```text
uv sync
uv run pytest
```

See [Local development (PyCharm)](docs/en/tutorials/local-dev-pycharm.md) / [Разработка локально](docs/ru/tutorials/local-dev-pycharm.md).
