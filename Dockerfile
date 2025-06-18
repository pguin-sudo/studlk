# <<< Builder >>>
FROM python:3.13-slim AS builder

# Обновление системы
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        gcc \
        libpq-dev \
        wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Настройка переменных окружения
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Установка зависимостей
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# <<< Runtime >>>
FROM python:3.13-slim AS base_server

# Установка необходимых пакетов
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей из builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# <<< Server >>>
FROM base_server AS studlk_server

WORKDIR /studlk
COPY . .

# Создание директории для логов
RUN mkdir -p /var/log/studlk_server

EXPOSE 8000