"""Основные роутера пакета."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("", summary="Health check")
async def health() -> JSONResponse:
    return JSONResponse("OK", 200)
