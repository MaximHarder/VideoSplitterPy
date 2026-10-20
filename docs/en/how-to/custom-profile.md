# Add or change a profile

## Goal

Save a split rule (and optional screenshots) under a name you can pass with `-p`.

## Steps

1. Open your config folder (see [settings](../reference/settings-yml.md)).
2. Copy `profiles/default.yml` to `profiles/<name>.yml` (for example `telegram.yml`).
3. Edit split mode, name template, and screenshot options. Full field list: [profile YAML](../reference/profile-yml.md).
4. Run:

```text
videosplitter -f movie.mp4 -p telegram
```

Or set `default_profile` in `settings.yml` to that name.

Flags such as `--split-by` still override the profile for one run without saving.
