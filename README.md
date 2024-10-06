## Шаблон приложения Напоминания о поездках

Для запуска проекта понадобится Poetry последней версии.
Желательно работать, используя WSL или Linux/MacOS.

[Устновка pipx](https://pipx.pypa.io/stable/installation/#installing-pipx:~:text=linux%2C%20and%20Windows.-,Installing%20pipx,-On%20macOS%3A)

[Установка poetry](https://python-poetry.org/docs/#installing-with-pipx)

Конфигурация poetry, чтобы виртуальное окружение создавалось в корневой директории с проектом:
```shell
poetry config virtualenvs.in-project true
```
В корневой директории проекта выполняем команду ниже, для установки зависимостей в виртуальное окружение:
```shell
poetry install
```
Для запуска проекта выполняем команду:
```shell
poetry run python -m app.main
```
