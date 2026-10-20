# Wizard (Textual menu)

Run `videosplitter` with no `-f` to open the interactive menu:

```text
+-----------------------------------------------------+
| 1. Settings                                         |
| 2. Split-Profiles                                   |
| 3. Start Split                                      |
+-----------------------------------------------------+
```

Built with Textual. UI text is English.

## 1. Settings

Edit and save `settings.yml` (ffmpeg path, extensions, remove source, temp dir, replace existing, output dir, recursive search, default profile). If ffmpeg/ffprobe cannot be found, you get an error asking you to set the path.

## 2. Split-Profiles

List profiles, create a new one from `default` (file name = translited slug with `-`), or delete a non-default profile. Full field editing can also be done in the YAML under `profiles/`.

## 3. Start Split

Dialog: path → profile → **Preview** (profile name, file count) → **Run**. Folders use bulk mode; recursive search comes from settings unless you use CLI flags with `-f`.

## CLI vs menu

With `-f`, the classic flag path runs (no menu). `--subfolders` / `-sf` overrides `recursive_search` from settings when you pass it.
