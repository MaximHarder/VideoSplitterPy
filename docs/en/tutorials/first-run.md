# First run

You use `videosplitter` when a video is too long or too heavy for one file. You pick a rule (a profile). The program cuts the video with FFmpeg and copies picture and sound — it does not re-encode them. The same command works on Windows, Linux, and macOS.

## What you need

- Python 3.11 or newer
- FFmpeg on the computer (`ffmpeg` and `ffprobe`). The settings file stores the path; the starting value `ffmpeg` means “use the one on PATH”
- For a text label on a screenshot: FFmpeg built with `drawtext`, and the font named in the profile must exist (default name: Times New Roman; on Linux you often need to install that font)

## Install

uv installs the package. There is no separate `uv install` step for this program.

From the repository:

```text
uv tool install .
videosplitter -f movie.mp4
```

`uv tool install .` reads the script entry in `pyproject.toml` (`videosplitter = "videosplitter.cli:main"`) and puts `videosplitter` on your PATH.

If the shell cannot find `videosplitter`, run `uv tool update-shell` and open a new terminal.

From a checkout, without a global install:

```text
uv run videosplitter -f movie.mp4
```

FFmpeg is not installed by uv — install it yourself.

## First split

```text
videosplitter -f movie.mp4
```

Or run with no flags for the menu:

```text
videosplitter
```

That opens the [wizard](../reference/wizard.md) (Settings / Profiles / Start Split).

The first run creates your config folder, `settings.yml`, and `profiles/default.yml` if they are missing. See [settings](../reference/settings-yml.md) and [profiles](../reference/profile-yml.md).

## Next steps

- [Split one file](../how-to/split-one-file.md)
- [Split a folder](../how-to/split-folder-bulk.md)
- [Develop locally / PyCharm](local-dev-pycharm.md)
