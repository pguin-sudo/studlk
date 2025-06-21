"""Подключение к основной БД через алхимию."""

import sys
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from studlk.core.config import settings
from studlk.core.logging import log


def create_database_url(docker: bool) -> URL:
    """Создает URL для подключения к базе данных.

    :return: URL: Объект URL для подключения к PostgreSQL.
    """
    return URL.create(
        drivername="postgresql+asyncpg",
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST_DOCKER if docker else settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_SCHEMA,
    )


def create_async_engine_and_session(
    url: str | URL,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """Создает асинхронный движок и фабрику сессий для PostgreSQL.

    :return: Кортеж (движок, фабрика сессий).

    :raise: SystemExit: При ошибке подключения.
    """

    try:
        engine = create_async_engine(
            url,
            echo=settings.DATABASE_ECHO,
            pool_size=10,
        )
    except Exception as e:  # noqa: BLE001
        log.error("Ошибка подключения к PostgreSQL: {}", e)
        sys.exit(1)

    # Фабрика сессий
    db_session = async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    return engine, db_session


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Генератор для получения сессии БД.

    :yield: AsyncSession: Асинхронная сессия PostgreSQL.
    """
    async with async_db_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# Инициализация подключения к PostgreSQL
SQLALCHEMY_DOCKER_DATABASE_URL = create_database_url(True)
SQLALCHEMY_DATABASE_URL = create_database_url(False)
async_engine, async_db_session = create_async_engine_and_session(
    SQLALCHEMY_DOCKER_DATABASE_URL,
)

# Аннотация для внедрения зависимости сессии
CurrentSession = Annotated[AsyncSession, Depends(get_session)]
