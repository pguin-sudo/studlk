# Aсинхронное веб приложение для учёта студентов - StudLK

## Способы запуска сервиса

### 1. Poetry (без БД): 
```sh
cp .env.example .env

poetry install
poetry run python studlk/run.py
```

### 2. Docker: 
```sh
# Создание .env файла из примера
cp .env.example .env

# Исправить .env для безопасности 
vim .env

# Запуск контейнеров (добвить -d для запуска в демон)
docker-compose up --build 

# Обновление состояние БД (при любых командах указывать путь к ini файлу из-за местоположения .env)
alembic -c studlk/alembic.ini upgrade head
```

## Работа с сервисом

### Логи
```sh
docker logs -t studlk_server
```

### Важные эндпоинты
- [Сваггер документация - http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)
- [API - http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)
- [Health - http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)