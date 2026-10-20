# settings.yml

## Где лежат файлы

- Windows: `%APPDATA%\videosplitter`
- Linux и macOS: `$XDG_CONFIG_HOME/videosplitter` или `~/.config/videosplitter`

Первый запуск создаёт недостающие `settings.yml` и `profiles/default.yml`. Уже существующие файлы не перезаписываются. Недостающие ключи при чтении берутся из текущих значений по умолчанию.

Другая папка: `VIDEOSPLITTER_CONFIG=...`.

## Поля

| Настройка | Смысл | По умолчанию |
| --- | --- | --- |
| ffmpeg | Путь или имя ffmpeg | `ffmpeg` из PATH |
| extensions | Расширения видео | `mp4`, `avi`, `flv`, `wmv`, `mkv` |
| remove_source | Удалить исходник после удачной нарезки | `false` |
| temp_dir | Временная папка | `{source_path}/.temp` |
| replace_existing | Перезаписывать выходные файлы | `true` |
| output_dir | Папка вывода | `{source_path}` |
| recursive_search | Искать во вложенных папках (TUI / без `-sf`) | `true` |
| default_profile | Профиль без `-p` | `default` |

`{source_path}` (и старый `{source_dir}`) — папка файла или корень bulk.
