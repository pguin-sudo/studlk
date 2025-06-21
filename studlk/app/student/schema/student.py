"""Схемы для студента из pydantic."""

from datetime import date
from enum import Enum
from typing import NewType

from pydantic import BaseModel, EmailStr, constr

PhoneStr = NewType("PhoneStr", constr(max_length=11))


# TODO: Перенести это куда-нибудь - мне не нравится зависимость модели от схемы
class StudentStatus(str, Enum):
    """Статусы студента."""

    ACTIVE = "Active"
    ACADEMIC_LEAVE = "Academic_leave"
    EXPELLED = "Expelled"
    GRADUATED = "Graduated"
    TRANSFERRED = "Transferred"


class StudentBaseSchema(BaseModel):
    """Базовая схема с общими полями студента."""

    first_name: str
    last_name: str
    birth_date: date
    status: StudentStatus = StudentStatus.ACTIVE
    contact_phone: PhoneStr | None = None
    email: EmailStr | None = None
    address: str | None = None
    scholarship: bool = False


class StudentCreateSchema(StudentBaseSchema):
    """Схема для создания нового студента."""


class StudentUpdateSchema(BaseModel):
    """Схема для обновления данных студента."""

    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None
    status: StudentStatus | None = None
    contact_phone: PhoneStr | None = None
    email: EmailStr | None = None
    address: str | None = None
    scholarship: bool | None = None


class StudentSchema(StudentBaseSchema):
    """Полная схема студента, включая read-only поля."""

    uuid: str

    class Config:
        from_attributes = True
