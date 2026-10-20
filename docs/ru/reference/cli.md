# Флаги CLI

Флаги подменяют профиль только на этот запуск. В файл они не пишутся.

```text
videosplitter -f movie.mp4
videosplitter -f ./videos --bulk
videosplitter -f ./videos --bulk --subfolders
videosplitter -f movie.mp4 -o D:\\out
videosplitter -f movie.mp4 -p telegram
videosplitter -f movie.mp4 -p telegram --split-by size --split-size 100
videosplitter -f movie.mp4 --split-by fixed --split-minutes 10
videosplitter -f movie.mp4 --split-by flexible --min-length 5 --max-length 10
videosplitter -f movie.mp4 --split-by parts --split-parts 4
```

| Флаг | Смысл |
| --- | --- |
| `-f` | Один файл или папка, если рядом есть `--bulk` |
| `--bulk` | Источник — папка. Для папки обязателен. Ошибка, если `-f` — файл |
| `--subfolders`, `-sf` | Только с `--bulk`. Искать во вложенных папках и повторить относительный путь в выводе |
| `-o` | Папка вывода на этот запуск |
| `-p` | Имя профиля. Важнее `default_profile` |
| `--split-by` | `size`, `fixed`, `flexible` или `parts` |
| `--split-size` | Мегабайты, для `size` |
| `--split-minutes` | Минуты одной части, для `fixed` |
| `--min-length`, `--max-length` | Минуты, для `flexible` |
| `--split-parts` | Число частей, для `parts`. Минимум 1 |

Без `-f` открывается [мастер](wizard.md).

Отдельного флага «указать папку настроек» нет. Другую папку задают переменной окружения `VIDEOSPLITTER_CONFIG` (путь к папке, где лежит `settings.yml`).
