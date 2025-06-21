"""Конфигурация приложения."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path().parent

# Пути
DOTENV = BASE_PATH / ".env"
LOG_DIR = BASE_PATH / "log"


class Settings(BaseSettings):
    """Основные настройки."""

    model_config = SettingsConfigDict(
        env_file=DOTENV,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # FastAPI
    FASTAPI_TITLE: str = "StudLK"
    FASTAPI_VERSION: str = "0.1.0"
    FASTAPI_DESCRIPTION: str = "Aсинхронное веб приложение для учёта студентов."
    FASTAPI_DOCS_URL: str = "/docs"

    # TODO: Добавить dev и prod environment

    # Подключение к БД
    DATABASE_NAME: str = "studlk"
    DATABASE_HOST: str = "localhost"
    DATABASE_HOST_DOCKER: str = "studlk_postgres"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = (
        "jNC5tfdUF2jAkpU3Ugt9SWPR7zGxKLjT9fLsdBQFaeMaKTW3kMgsFScCpjx8YKtb"
    )

    # Конфигурация алхимии
    DATABASE_ECHO: bool = False
    DATABASE_POOL_ECHO: bool = False
    DATABASE_SCHEMA: str = "studlk"
    DATABASE_CHARSET: str = "utf8mb4"

    # Данные часового пояса
    TIMEZONE: str = "UTC"
    DATETIME_TIMEZONE: str = TIMEZONE
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # Логирование
    LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(message)s"
    LOG_FILE_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(message)s"
    LOG_FILENAME: str = "studlk.log"
    LOG_LEVEL: str = "DEBUG"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
