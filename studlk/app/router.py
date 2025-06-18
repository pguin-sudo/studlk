"""Подключение всех роутеров."""

from fastapi import APIRouter

from studlk.app.student.api.router import v1 as student_v1

main_router = APIRouter()

main_router.include_router(student_v1)
