# Мастер (меню Textual)

`videosplitter` без `-f` открывает меню:

```text
+-----------------------------------------------------+
| 1. Settings                                         |
| 2. Split-Profiles                                   |
| 3. Start Split                                      |
+-----------------------------------------------------+
```

Интерфейс на английском, на Textual.

## 1. Settings

Правка и сохранение `settings.yml`. Если `ffmpeg`/`ffprobe` не находятся — ошибка с просьбой задать путь.

## 2. Split-Profiles

Список, создание из `default` (имя файла — slug через translited с `-`), удаление (кроме `default`). Полные поля можно править в YAML.

## 3. Start Split

Путь → профиль → Preview → Run. Для папки — bulk; recursive из settings, если не заданы флаги CLI с `-f`.

С `-f` меню не открывается. `--subfolders` важнее `recursive_search`.
