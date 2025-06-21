"""Модель студента для БД."""

from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from studlk.app.student.schema.student import StudentStatus
from studlk.common.model import Base, id_key


class Student(Base):
    """Таблица студентов."""

    uuid: Mapped[id_key] = mapped_column(init=False)

    # Основная информация с индексами для часто используемых полей в WHERE
    # (в последствии и JOIN) запросах
    first_name: Mapped[str] = mapped_column(String(64), comment="Имя студента")
    last_name: Mapped[str] = mapped_column(String(64), comment="Фамилия студента")
    birth_date: Mapped[date] = mapped_column(
        Date(),
        index=True,
        comment="Дата рождения",
    )
    status: Mapped[StudentStatus] = mapped_column(
        Enum(StudentStatus, create_type=True),
        default=StudentStatus.ACTIVE,
        index=True,
        comment="Статус студента",
    )

    # Дополнительная информация
    contact_phone: Mapped[str | None] = mapped_column(
        String(11),
        default=None,
        index=True,
        comment="Контактный телефон",
    )
    email: Mapped[str | None] = mapped_column(
        String(50),
        default=None,
        unique=True,
        index=True,
        comment="Электронная почта",
    )
    address: Mapped[str | None] = mapped_column(
        String(128),
        default=None,
        comment="Адрес проживания",
    )
    scholarship: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="Получает стипендию",
    )
