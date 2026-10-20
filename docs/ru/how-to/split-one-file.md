# Нарезать один файл

## Цель

Разрезать одно видео по профилю или разовым флагам.

## Шаги

1. Установите программу или используйте `uv run` (см. [Первый запуск](../tutorials/first-run.md)).
2. Запустите с `-f`:

```text
videosplitter -f movie.mp4
```

3. По желанию: профиль, папка вывода или подмена нарезки:

```text
videosplitter -f movie.mp4 -p telegram
videosplitter -f movie.mp4 -o D:\\out
videosplitter -f movie.mp4 --split-by size --split-size 100
videosplitter -f movie.mp4 --split-by fixed --split-minutes 10
videosplitter -f movie.mp4 --split-by flexible --min-length 5 --max-length 10
videosplitter -f movie.mp4 --split-by parts --split-parts 4
```

Флаги меняют профиль только на этот запуск и не переписывают YAML.

## Заметки

- Если путь — папка, нужен `--bulk` (см. [папка bulk](split-folder-bulk.md)).
- Полный список флагов: [CLI](../reference/cli.md).
