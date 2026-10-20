# Local development (PyCharm)

This lesson gets a checkout of VideoSplitterPy running on your machine, including PyCharm.

## 1. Clone and sync

```text
cd /path/to/VideoSplitterPy
uv sync
```

uv creates `.venv` and installs the package plus dev tools (pytest).

## 2. Interpreter in PyCharm

1. Open the project folder in PyCharm.
2. Settings → Project → Python Interpreter → Add → Existing.
3. Pick `.venv/bin/python` (Windows: `.venv\\Scripts\\python.exe`).

PyCharm should mark the project as using that environment.

## 3. Run the command

**Terminal in PyCharm** (or any shell in the project root):

```text
uv run videosplitter
```

You should see `Path: ` right away. Press Enter on an empty path to get `path not found` on the error stream.

With a file:

```text
uv run videosplitter -f /path/to/movie.mp4
```

**Run configuration (optional):** Module name `videosplitter`, or script path to the installed console script; working directory = project root. Add parameters such as `-f movie.mp4` when you want flags instead of the wizard.

## 4. Tests

```text
uv run pytest
```

Or only the CLI tests:

```text
uv run pytest tests/test_cli.py
```

In PyCharm: right-click `tests/` → Run pytest.

## 5. Config for tests and experiments

Point the program at a temporary config folder:

```text
export VIDEOSPLITTER_CONFIG=/tmp/videosplitter-dev
uv run videosplitter -f movie.mp4
```

See [settings](../reference/settings-yml.md).
