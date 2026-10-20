# Разработка локально (PyCharm)

Как поднять рабочую копию VideoSplitterPy на своей машине, в том числе в PyCharm.

## 1. Клон и sync

```text
cd /path/to/VideoSplitterPy
uv sync
```

uv создаёт `.venv` и ставит пакет плюс инструменты разработки (pytest).

## 2. Интерпретатор в PyCharm

1. Откройте папку проекта в PyCharm.
2. Settings → Project → Python Interpreter → Add → Existing.
3. Укажите `.venv/bin/python` (Windows: `.venv\\Scripts\\python.exe`).

## 3. Запуск команды

**Терминал в PyCharm** (или любая оболочка в корне проекта):

```text
uv run videosplitter
```

Сразу должно появиться `Path: `. Пустой Enter даёт `path not found` в потоке ошибок.

С файлом:

```text
uv run videosplitter -f /path/to/movie.mp4
```

**Конфигурация Run (по желанию):** модуль `videosplitter` или путь к консольному скрипту; рабочая папка — корень проекта. Параметры вроде `-f movie.mp4`, если нужны флаги вместо мастера.

## 4. Тесты

```text
uv run pytest
```

Только CLI:

```text
uv run pytest tests/test_cli.py
```

В PyCharm: правый клик по `tests/` → Run pytest.

## 5. Свои настройки для опытов

```text
export VIDEOSPLITTER_CONFIG=/tmp/videosplitter-dev
uv run videosplitter -f movie.mp4
```

См. [настройки](../reference/settings-yml.md).
