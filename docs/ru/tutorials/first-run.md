# Первый запуск

Программа `videosplitter` нужна, когда ролик слишком длинный или слишком тяжёлый для одного файла. Вы выбираете правило (профиль). Программа режет видео через FFmpeg и копирует картинку и звук — без перекодирования. Одна и та же команда работает в Windows, Linux и macOS.

## Что нужно заранее

- Python 3.11 или новее
- FFmpeg на компьютере (`ffmpeg` и `ffprobe`). Путь лежит в настройках; стартовое значение `ffmpeg` значит «взять ту, что уже есть в PATH»
- Для подписи на кадре: FFmpeg с фильтром `drawtext` и файл шрифта из профиля (по умолчанию Times New Roman; в Linux его часто нужно поставить отдельно)

## Установка

Установщик — uv. Отдельной команды `uv install` для этой программы нет.

Из папки репозитория:

```text
uv tool install .
videosplitter -f movie.mp4
```

`uv tool install .` читает точку входа в `pyproject.toml` (`videosplitter = "videosplitter.cli:main"`) и кладёт `videosplitter` в PATH.

Если оболочка не находит команду, выполните `uv tool update-shell` и откройте терминал заново.

Из рабочей копии без глобальной установки:

```text
uv run videosplitter -f movie.mp4
```

FFmpeg uv не ставит — его нужно установить отдельно.

## Первая нарезка

```text
videosplitter -f movie.mp4
```

Или без флагов — меню:

```text
videosplitter
```

Откроется [мастер](../reference/wizard.md) (Settings / Profiles / Start Split).

Первый запуск создаёт папку настроек, `settings.yml` и `profiles/default.yml`, если их ещё нет. См. [настройки](../reference/settings-yml.md) и [профили](../reference/profile-yml.md).

## Дальше

- [Нарезать один файл](../how-to/split-one-file.md)
- [Нарезать папку](../how-to/split-folder-bulk.md)
- [Разработка локально / PyCharm](local-dev-pycharm.md)
