# VideoSplitterPy

This guide explains the `videosplitter` program in plain language. The command is the `videosplitter` package in this repository. Where the plan is still open, this page follows the latest version of that plan.

You use it when a video is too long or too heavy for one file. You pick a rule, called a profile. The program cuts the video into parts with FFmpeg. It copies the picture and sound. It does not re-encode them.

The same command works on Windows and on Unix (Linux and macOS).

## What you need

- Python 3.11 or newer.
- FFmpeg on the computer, including `ffmpeg` and `ffprobe`. The settings file stores the path. The starting value is the name `ffmpeg`, which means “use the one on PATH”.
- For a text label on a screenshot, FFmpeg must be built with `drawtext`, and the font file named in the profile must exist. Times New Roman is the default font name. On Linux that font is often missing until you install it.

The console command is `videosplitter`.

## Install with uv

uv is the installer. There is no separate `uv install` step for this program.

From the repository, after the package exists:

```text
uv tool install .
videosplitter -f movie.mp4
```

`uv tool install .` reads the script entry in `pyproject.toml` and puts `videosplitter` on your PATH. The entry is `videosplitter = "videosplitter.cli:main"`.

If the shell cannot find `videosplitter`, run `uv tool update-shell` and open a new terminal. That adds uv’s tool folder to PATH.

From a checkout, without installing the command globally:

```text
uv run videosplitter -f movie.mp4
```

FFmpeg still has to be installed yourself. uv does not install it.

## Where your files live

The program does not store your settings inside its install folder.

- Windows: `%APPDATA%\videosplitter`
- Linux and macOS: `$XDG_CONFIG_HOME/videosplitter`, or `~/.config/videosplitter` when that variable is empty

Inside that folder:

- `settings.yml` is the program settings.
- `profiles/default.yml` is the profile used when you do not name another one.
- `profiles/<name>.yml` is any extra profile. `<name>` is the name you pass with `-p`.

The first run creates this folder, `settings.yml`, and `profiles/default.yml` if they are missing.

There is no flag to point at a different config folder.

## Settings

`settings.yml` holds choices that apply to every run, until a flag overrides one of them for that run only.

| Setting | Meaning | Starting value |
| --- | --- | --- |
| FFmpeg path | Program that cuts the video and reads its length | `ffmpeg` on PATH |
| Video extensions | Which files count as video | `mp4`, `avi`, `flv`, `wmv`, `mkv` |
| Remove source | Delete the original after a successful split | off |
| Temp dir | Where a part is written before it is moved into place | the system temp directory |
| Replace existing | Overwrite an output file that is already there | off |
| Output dir | Where finished parts go | `{source_dir}` |
| Default profile | Profile name used when you omit `-p` | `default` |

`{source_dir}` is a placeholder, not a real folder name.

- For one file, it means the folder that contains that file.
- For `--bulk`, it means the folder you passed as the source.

Example:

```yaml
ffmpeg: ffmpeg
extensions:
  - mp4
  - avi
  - flv
  - wmv
  - mkv
remove_source: false
temp_dir: ""
replace_existing: false
output_dir: "{source_dir}"
default_profile: default
```

An empty `temp_dir` means the system temp directory.

Extensions are matched without caring about letter case. `MP4` and `mp4` are the same.

## Profiles

A profile is one saved way to split. It lives in `profiles/<name>.yml`.

The shipped `default` profile:

- splits by size
- limit 1800 MB
- minimum part length 1 minute
- screenshots off
- part name `{video_name}_p{part|pad(2)}.{ext}`

You can add as many profiles as you want. A flag such as `--split-by` changes the profile for that run only. It does not rewrite the YAML file.

### Minimum part length

If the whole video is shorter than this length, the program does not split it. It writes no parts, takes no screenshot, and does not delete the source.

The starting value is 1 minute. A 40-second clip stays as it is.

This check is separate from the flexible-time minimum below.

### Split by size

You set a size in MB. The program counts:

`n = ceil(file bytes / (limit MB × 1024 × 1024))`

- `n` of 1 or less: do not split. A file that already fits the limit is left alone.
- `n` of 2 or more: `n` parts of equal time. The last part ends at the real end of the video, so no time is dropped.

Example: a 3000 MB file and a limit of 1800 MB gives `ceil(3000 / 1800) = 2`. You get two parts of equal length.

The cut is by time, not by watching the byte count of each piece. If the video is denser at the end, the last file can be larger than the limit.

### Split by fixed time

You set how many minutes one part may contain.

- If the video fits in one slice, it is not split.
- Otherwise each part is that many minutes, and the last part is whatever time is left.

The last piece is allowed to be shorter than the minimum part length. The minimum part length only stops a split when the whole video is shorter than that floor.

Example: 50 minutes, slice of 30 minutes. You get 30 minutes, then 20 minutes.

### Split by flexible time

You set a minimum and a maximum length for a part, in minutes.

- If the video is shorter than the profile’s minimum part length (the 1-minute floor by default), it is not split.
- If the video is at or under the flexible maximum, it is not split. It already fits in one part.
- Otherwise `n = ceil(duration / max)` and every part is `duration / n`.
- If that shared length is still shorter than the flexible minimum, the program stops with an error. There is no way to satisfy both numbers.

Example: 23 minutes, minimum 5, maximum 10. `ceil(23 / 10) = 3`, and `23 / 3` is about 7.7 minutes. All three parts sit inside 5 to 10.

Example that fails: 11 minutes, minimum 8, maximum 10. Two parts would be 5.5 minutes, which is under 8. One part would be 11, which is over 10.

### Split by parts

You set how many parts you want. The number has to be at least 1.

- `1` means do not split.
- `2` or more means that many parts of equal time.

Example: `--split-parts 4` on a 40-minute video gives four parts of 10 minutes.

## Names

The part filename comes from a template. Tags sit in curly braces.

| Tag | Meaning |
| --- | --- |
| `{video_name}` | Source file name without the extension |
| `{file_name}` | Same stem. Used on screenshot labels |
| `{ext}` | Source extension, without the dot |
| `{part}` | This part’s number, starting at 1 |
| `{parts}` | How many parts this video became |

You can pipe a tag through a function: `{video_name|uppercase}`.

Text functions:

| Function | Effect |
| --- | --- |
| `translited` | Rewrites the text into Latin letters |
| `uppercase` | Capital letters |
| `lowercase` | Small letters |

Number functions:

| Function | Effect |
| --- | --- |
| `pad(2)` | At least two digits: `1` becomes `01` |
| `int` | Whole number |
| `round(2)` | Two digits after the decimal point |

Functions can be chained: `{video_name|translited|lowercase}`.

The default template is `{video_name}_p{part|pad(2)}.{ext}`. A file `Holiday.mp4` split into two parts becomes `Holiday_p01.mp4` and `Holiday_p02.mp4`.

On a screenshot label, `[is_final]...[/is_final]` is kept only for the last part. The text between the markers is dropped for every earlier part. The default label template is `{part},[is_final][/is_final],{file_name}`. With an empty marker, the last part still has the two commas.

## Screenshots

Screenshots are off in the default profile. Turn them on per profile.

```yaml
create_screenshot: false
screenshot_time: "50% of the part"
screenshot_name: "{video_name}_p{part|pad(2)}"
screenshot_format: jpg
write_label: false
label_template: "{part},[is_final][/is_final],{file_name}"
label_font: "Times New Roman"
label_size_px: 13
label_color: white
label_position:
  bottom: 15
  right: 5
label_border_px: 2
label_border_color: black
```

### When

`screenshot_time` is one of these:

| Value | Frame |
| --- | --- |
| `first frame of the part` | Start of this part |
| `last frame of the part` | End of this part |
| `random frame of the part` | A random instant inside this part |
| `50% of the part` | Halfway through this part. Any whole percent from 0 to 100 works. 0 is the first frame, 100 is the last |
| `first frame of the video` | Start of the original file |
| `last frame of the video` | End of the original file |
| `random frame of the video` | A random instant in the original file |
| `50% of the video` | Halfway through the original file. Again, 0 to 100 |

The starting value is `50% of the part`.

A percent below 0 or above 100 is an error.

Random means “anywhere from the start of that span up to, but not including, the end.” Tests pin the instant so the result does not change between runs. A normal run does not.

### File name and format

`screenshot_name` uses the same tags as the part name. The starting value is the part’s base name, so the image sits next to the part and shares that base name.

`screenshot_format` is `jpg`, `png`, or `webp`. The starting value is `jpg`. The extension on disk is this format, not `{ext}`.

A part named `Holiday_p01.mp4` with the defaults gets `Holiday_p01.jpg` in the same folder.

### Label

`write_label` is yes or no. No leaves the frame as FFmpeg grabbed it.

Yes draws the label with FFmpeg `drawtext`. There is no separate image library.

- Font: Times New Roman, unless you change `label_font`.
- Size: 13 px.
- Color: white.
- Border: 2 px, black.

Position uses one vertical side and one horizontal side.

- Vertical is `top` or `bottom`. The start is `bottom: 15` (15 px).
- Horizontal is `left` or `right`. The start is `right: 5` (5 px).

Leave a side out and it is not used. If you write both `top` and `bottom`, the first one in the file wins and the other is removed. The same rule applies to `left` and `right`. The first key on an axis is the one that sets the margin.

If the label is on and the font file cannot be found, that video fails. If this FFmpeg cannot write the chosen image format, that video fails too.

A video that is not split does not get a screenshot.

## Commands

Flags you pass on the command line override the profile for that run. They do not save.

```text
videosplitter -f movie.mp4
videosplitter -f ./videos --bulk
videosplitter -f ./videos --bulk --subfolders
videosplitter -f movie.mp4 -o D:\out
videosplitter -f movie.mp4 -p telegram
videosplitter -f movie.mp4 -p telegram --split-by size --split-size 100
videosplitter -f movie.mp4 --split-by fixed --split-minutes 10
videosplitter -f movie.mp4 --split-by flexible --min-length 5 --max-length 10
videosplitter -f movie.mp4 --split-by parts --split-parts 4
```

| Flag | Meaning |
| --- | --- |
| `-f` | One file, or a folder when you also pass `--bulk` |
| `--bulk` | The source is a folder. Required for a folder. An error if `-f` is a file |
| `--subfolders`, `-sf` | With `--bulk` only. Also search child folders, and rebuild that relative path under the output folder |
| `-o` | Output folder for this run |
| `-p` | Profile name. Wins over `default_profile` |
| `--split-by` | `size`, `fixed`, `flexible`, or `parts` |
| `--split-size` | MB, for `size` |
| `--split-minutes` | Minutes in one part, for `fixed` |
| `--min-length`, `--max-length` | Minutes, for `flexible` |
| `--split-parts` | How many parts, for `parts`. Minimum 1 |

`--bulk` without `--subfolders` reads only the folder you named, not its children.

`--subfolders` without `--bulk` is not a valid command.

With `--subfolders`, a file at `videos/trip/day1/clip.mp4` is written under `output/trip/day1/`. The folder `videos` is the bulk root, so it is not repeated.

## Wizard

Run `videosplitter` with no `-f` to open the wizard. It asks for the same facts the flags set: the file or folder, bulk and subfolders, the profile or the split numbers, and the output folder. It calls the same planner as the command. It does not write those answers back into the YAML unless you are editing settings on purpose. The program prints these prompts in English, in this order:

1. `Path: `
2. `Include subfolders? [y/n]: ` only when the path is a directory
3. `Profile name (empty for default): `
4. `Override split mode? [y/n]: `
5. When the answer is `y`: `Split by [size/fixed/flexible/parts]: `, then `MB: ` for size, `Minutes: ` for fixed, `Minimum minutes: ` and `Maximum minutes: ` for flexible, or `Parts: ` for parts
6. `Output directory (empty for settings): `

## What a run does

1. Load settings. Create the default files on the first run.
2. Load the profile: `-p` if you passed it, otherwise `default_profile`. Apply any `--split-by` overrides on top.
3. Collect files. One `-f` file, or the folder for `--bulk`, plus child folders when `-sf` is set. Skip names whose extension is not in the list.
4. For each video, read the length with `ffprobe` and the size from the file.
5. Ask the planner for parts, or for “do not split”.
6. If there is no split, stop for that file. Leave it on disk.
7. For each part, build the name, write it with `ffmpeg -c copy` in the temp folder, then move it to the output folder. Copy means the part is a cut, not a new encode.
8. If replace is off and that output name already exists, leave the old file and move on. That is not a failure.
9. If a part fails, stop that video, delete the temp file, and do not delete the source.
10. If every part of that video succeeded and at least one new file was written, delete the source only when remove-source is on.
11. If screenshots are on, write the image after the part file is in place. A screenshot failure fails that video the same way a bad part does.

## When it will not split

- The video is shorter than the minimum part length (1 minute unless you change it).
- Size mode and the file already fits in the limit.
- Fixed time and the video fits in one slice.
- Flexible time and the video fits under the maximum.
- Parts mode and you asked for one part.
- The extension is not in the settings list. In a folder, that file is ignored.

Flexible time can also error when the minimum and maximum cannot both be met. That is a failure, not a silent skip.

## Words

| Word | Meaning |
| --- | --- |
| Profile | A YAML file with one split rule, a name template, and screenshot choices |
| Part | One time range cut from the source |
| Planner | The piece that decides the time ranges. It does not call FFmpeg |
| Stream copy | FFmpeg `-c copy`: cut without re-encoding |
| Bulk | Split every matching video in a folder |
| `{source_dir}` | The source folder used in the output path |
