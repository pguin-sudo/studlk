"""Создание приложения."""

from fastapi import FastAPI

from studlk.app.router import main_router
from studlk.core.config import settings
from studlk.core.logging import log, setup_logging


def register_app() -> FastAPI:
    app = FastAPI(
        title=settings.FASTAPI_TITLE,
        version=settings.FASTAPI_VERSION,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
    )

    setup_logging()
    register_router(app)

    log.info("App is starting")

    return app


def register_router(app: FastAPI) -> None:
    app.include_router(main_router)


app = register_app()
