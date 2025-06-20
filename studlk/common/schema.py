"""Стандартные схемы приложения."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from studlk.core.config import settings

# TODO: добавить модели номера и почты


class SchemaBase(BaseModel):
    """Стандартная пайдантиковская схема.

    Добавлена для соглования времени с форматом из конфига
    """

    model_config = ConfigDict(
        json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)},
        use_enum_values=True,
    )
