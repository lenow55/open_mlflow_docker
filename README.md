# Open Mlflow Docker

## Назначение

Репозиторий, с описанием докер контейнеров, которые
используются в [open-mlflow-infra](https://github.com/lenow55/open_mlflow_infra)

## Структура репозитория

```txt
  open_mlflow_docker
 ├╴  mlflow
 │ ├╴  Dockerfile - манифест образа для mlflow сервера
 │ ├╴  poetry.lock - лок зависимостей
 │ └╴  pyproject.toml
 ├╴  sql_initer
 │ ├╴  Dockerfile - манифест образа для инициализации баз
 │ ├╴  config.py - класс конфигурации для инициализации баз
 │ ├╴  example_configs.json - json список с базами данных для проектов
open_mlflow_docker пример
 │ ├╴  main.py - основной код подключения и создания баз
 │ ├╴  poetry.lock - лок зависимостей
 │ └╴  pyproject.toml
 └╴  README.md
```

## Сборка

### Сервер mlflow

```bash
docker build -t lenow/mlflow-server:v... -t lenow/mlflow-server:latest ./mlflow \
&& docker push lenow/mlflow-server:v... \
&& docker push lenow/mlflow-server:latest
```

### Инициализатор базы

```bash
docker build -t lenow/sql-initer:v... -t lenow/sql-initer:latest ./sql_initer \
&& docker push lenow/sql-initer:v... \
&& docker push lenow/sql-initer:latest
```
