# settings.yml

## Where files live

- Windows: `%APPDATA%\videosplitter`
- Linux and macOS: `$XDG_CONFIG_HOME/videosplitter`, or `~/.config/videosplitter`

Inside: `settings.yml`, `profiles/default.yml`, other `profiles/<name>.yml`.

First run creates missing `settings.yml` and `profiles/default.yml`. Existing files are not overwritten. Missing keys are filled from current defaults when reading.

Override folder: `VIDEOSPLITTER_CONFIG=/path/to/config-folder`.

## Fields

| Setting | Meaning | Default |
| --- | --- | --- |
| ffmpeg | Path or name of ffmpeg | `ffmpeg` on PATH |
| extensions | Video extensions | `mp4`, `avi`, `flv`, `wmv`, `mkv` |
| remove_source | Delete source after a successful split | `false` |
| temp_dir | Temp folder for parts | `{source_path}/.temp` |
| replace_existing | Overwrite existing outputs | `true` |
| output_dir | Default output folder | `{source_path}` |
| recursive_search | Search subfolders in bulk (TUI / when CLI omits `-sf`) | `true` |
| default_profile | Profile when `-p` is omitted | `default` |

`{source_path}` (and legacy `{source_dir}`) is the source file’s folder, or the bulk root folder.

Example:

```yaml
ffmpeg: ffmpeg
extensions: [mp4, avi, flv, wmv, mkv]
remove_source: false
temp_dir: "{source_path}/.temp"
replace_existing: true
output_dir: "{source_path}"
recursive_search: true
default_profile: default
```
