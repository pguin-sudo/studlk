"""Основные эндпоинты версии."""

from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import and_, or_, select

from studlk.app.student.model.student import Student
from studlk.app.student.schema.student import (
    StudentCreateSchema,
    StudentStatus,
    StudentUpdateSchema,
)
from studlk.common.response import SchemaResponseModel
from studlk.database.db import CurrentSession

router = APIRouter()


# TODO: Перевести пагинацию в зависимости
@router.get("/", response_model=SchemaResponseModel[List[Student]])
async def get_students(
    db: CurrentSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[StudentStatus] = None,
    min_birth_date: Optional[date] = None,
    max_birth_date: Optional[date] = None,
    has_scholarship: Optional[bool] = None,
    search: Optional[str] = None,
):
    """Получить список студентов с пагинацией и фильтрами."""
    stmt = select(Student).offset(skip).limit(limit)

    filters = []
    if status:
        filters.append(Student.status == status)
    if min_birth_date:
        filters.append(Student.birth_date >= min_birth_date)
    if max_birth_date:
        filters.append(Student.birth_date <= max_birth_date)
    if has_scholarship is not None:
        filters.append(Student.scholarship == has_scholarship)
    if search:
        filters.append(
            or_(
                Student.first_name.ilike(f"%{search}%"),
                Student.last_name.ilike(f"%{search}%"),
            ),
        )

    if filters:
        stmt = stmt.where(and_(*filters))

    result = await db.execute(stmt)
    students = result.scalars().all()

    return {"code": 200, "data": students}


@router.post("/", response_model=SchemaResponseModel[Student], status_code=201)
async def create_student(
    db: CurrentSession,
    student_data: StudentCreateSchema,
):
    """Создать нового студента."""
    student = Student(**student_data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return {"code": 201, "data": student}


@router.get("/{student_id}", response_model=SchemaResponseModel[Student])
async def get_student(
    db: CurrentSession,
    student_id: UUID,
):
    """Получить студента по UUID."""
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"code": 200, "data": student}


@router.put("/{student_id}", response_model=SchemaResponseModel[Student])
async def update_student(
    db: CurrentSession,
    student_id: UUID,
    student_data: StudentUpdateSchema,
):
    """Обновить данные студента."""
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)
    return {"code": 200, "data": student}


@router.delete("/{student_id}", status_code=204)
async def delete_student(
    db: CurrentSession,
    student_id: UUID,
):
    """Удалить студента."""
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()
    return {"code": 200, "data": None}


@router.delete("/by-status/{status}", response_model=SchemaResponseModel[int])
async def delete_students_by_status(
    db: CurrentSession,
    status: StudentStatus,
):
    """Удалить всех студентов с указанным статусом."""
    stmt = select(Student).where(Student.status == status)
    result = await db.execute(stmt)
    students = result.scalars().all()

    for student in students:
        await db.delete(student)

    await db.commit()
    return {"code": 201, "data": len(students)}


@router.get("/by-email/{email}", response_model=SchemaResponseModel[Student])
async def get_student_by_email(
    db: CurrentSession,
    email: str,
):
    """Получить студента по email."""
    stmt = select(Student).where(Student.email == email)
    result = await db.execute(stmt)
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"code": 200, "data": student}
