# app/schemas/table_type.py
# DTO-схемы Pydantic для типа столика

from typing import Optional
from pydantic import BaseModel, Field


# Общие поля
class TableTypeBase(BaseModel):
    seats: int = Field(gt=0)
    location: str


# Схема для создания
class TableTypeCreate(TableTypeBase):
    pass


# Схема для обновления — все поля опциональны
class TableTypeUpdate(BaseModel):
    seats: Optional[int] = None
    location: Optional[str] = None


# Схема для ответа
class TableTypeRead(TableTypeBase):
    id: int

    model_config = {"from_attributes": True}