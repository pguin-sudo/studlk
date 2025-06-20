"""Стандартные модели приложения."""

import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import UUID, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    declared_attr,
    mapped_column,
)

id_key = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
        comment="UUID PK",
    ),
]


class DateTimeMixin(MappedAsDataclass):
    """Миксин с датами создания и обновления."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=datetime.now,
        comment="Record creation timestamp",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        init=False,
        onupdate=datetime.now,
        comment="Record update timestamp",
    )


class MappedBase(AsyncAttrs, DeclarativeBase):
    """Базовая модель для всех таблиц."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        """Имя таблицы по умолчанию равно имени класса."""
        return cls.__name__.lower()

    @declared_attr.directive
    def __table_args__(cls) -> dict:  # noqa: N805
        """Комментарий к таблице берется из докстринги класса."""
        return {"comment": cls.__doc__ or ""}


class Base(MappedBase, DateTimeMixin):
    """База от которой должны наследоваться все модели таблиц.

    Включает в себя:
    - UUID PK
    - Даты создания/обновления
    """

    __abstract__ = True
