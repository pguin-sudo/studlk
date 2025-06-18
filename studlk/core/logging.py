"""Логгер."""

import logging

from studlk.core.config import LOG_DIR, settings


def setup_logging() -> None:
    """Базовая настройка логирования в консоль."""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
        handlers=[logging.StreamHandler()],
    )


def set_logfile() -> None:
    """Настройка записи логов в простые файлы без ротации."""
    LOG_DIR.mkdir(exist_ok=True)

    access_handler = logging.FileHandler(
        filename=(LOG_DIR / settings.LOG_FILENAME),
        encoding="utf-8",
    )
    access_handler.setLevel(settings.LOG_FORMAT)
    access_handler.setFormatter(logging.Formatter(settings.LOG_FILE_FORMAT))
    access_handler.addFilter(lambda r: r.levelno <= logging.INFO)

    # Добавляем обработчики
    logging.getLogger().addHandler(access_handler)


# Глобальный логгер
log = logging.getLogger(__name__)
