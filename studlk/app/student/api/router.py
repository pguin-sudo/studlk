"""Подключение роутеров версионирования."""

from fastapi import APIRouter

from studlk.app.common.health import router as health_router
from studlk.app.student.api.v1.student import router as sudent_router

v1 = APIRouter(prefix="/api/v1")

# Стандартные эндпоинты
v1.include_router(health_router, prefix="/health", tags=["common"])

# Эндоинты API
v1.include_router(sudent_router, prefix="/student", tags=["student"])
