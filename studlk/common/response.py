from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    """Универсальная модель возвращаемых данных."""

    # TODO: Добавить поле msg с переведенными сообщениями
    code: int = Field(200)
    data: Any | None = Field(None)


SchemaT = TypeVar("SchemaT")


class SchemaResponseModel(ResponseModel, Generic[SchemaT]):
    """Универсальная модель возвращаемых данных с дженериком схемы."""

    data: SchemaT
