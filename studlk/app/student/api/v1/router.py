"""Подключение роутеров студентов."""

from fastapi import APIRouter

from studlk.app.student.api.v1.student import router as student_router

v1 = APIRouter(prefix="/api/v1")

v1.include_router(student_router, prefix="/student", tags=["student"])
