# Как редактировать проект

## Первичная настройка

После установки движка, следует сделать следующее:

1. Установить [VsCode](https://code.visualstudio.com/)
2. Установить расширение godot-tools
3. Настроить расширение в соответствии с [инструкцией](https://github.com/godotengine/godot-vscode-plugin?tab=readme-ov-file#configuration)
4. Установить расширение GitLens
5. Установить Python
6. Создать в корне проекта виртуальное окружение `python -m venv .venv`
7. Установить расширения Python и Python Environment
8. Открыть терминал (виртуальное окружение должно активироваться автоматически), установить зависимости `pip install -r requirements.txt`
9. Выставить commit hooks: `pre-commit install`

## Процесс изменения проекта

Внедрение фичи в проект состоит из следующих этапов

1. Заведение тикета в статусе "In Progress". Все тикеты должны создаваться после совместного обсуждения командой, или являться подтикетами таких тикетов;
2. Создание ветки фичи. Ветку делаем напрямую от `master`, никаких `dev`-веток. Название ветки стоит формировать по схеме `<board>/<issue-number>`. Например, для тикета #101 на доске Prototypes ветку стоит назвать `prototypes/101`
3. Внесение изменений в проект внутри ветки.
4. Форматирование исходников командой `gdformat scripts/` и исправление ошибок, которые выпишет `gdlint scripts/`. Не сделав это, pr вмерджить не получится. Чтобы точно этого не забывать, стоит выставить commit hooks ([Первичная настройка](#первичная-настройка), п. 9)
5. Push, создание Pull Request. В случае падения static-checks, возврат к п. 4. В случае наличия конфликтов - [решить конфликты](../how_to_solve_conflicts.md), а затем возврат к п. 3
6. Merge Pull Request. Ветка удалится автоматически.
7. Локально `git checkout master` и `git pull`.

## Ошибки линтера

Сообщения линтера не отличаются подробностью. Чтобы эффективно их исправлять, необходимо ознакомиться с [документацией](https://github.com/Scony/godot-gdscript-toolkit/wiki/3.-Linter) линтера.

Для удобства сюда из документации линтера продублирован *ожидаемый порядок объявлений в классе*:

- `tool`
- `classname`
- `extends`
- signals
- enums
- constants
- exports
- public variables
- private variables (prefixed with underscore `_`)
- `onready` public variables
- `onready` private variables (prefixed with underscore `_`)
- other statements