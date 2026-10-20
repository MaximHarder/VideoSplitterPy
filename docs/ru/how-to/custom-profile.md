# Свой профиль

## Цель

Сохранить правило нарезки (и кадры) под именем для `-p`.

## Шаги

1. Откройте папку настроек (см. [настройки](../reference/settings-yml.md)).
2. Скопируйте `profiles/default.yml` в `profiles/<имя>.yml` (например `telegram.yml`).
3. Правьте режим нарезки, шаблон имени и кадры. Поля: [профиль YAML](../reference/profile-yml.md).
4. Запуск:

```text
videosplitter -f movie.mp4 -p telegram
```

Или укажите это имя в `default_profile` в `settings.yml`.

Флаги вроде `--split-by` по-прежнему подменяют профиль на один запуск без записи в файл.
