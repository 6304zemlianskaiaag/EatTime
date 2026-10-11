# app/schemas/place.py
# DTO-схемы Pydantic для столика

from typing import Optional
from pydantic import BaseModel


# Общие поля
class PlaceBase(BaseModel):
    type_table_id: int
    restaurant_id: int
    is_active: bool = True


# Схема для создания
class PlaceCreate(PlaceBase):
    pass


# Схема для обновления
class PlaceUpdate(BaseModel):
    type_table_id: Optional[int] = None
    restaurant_id: Optional[int] = None
    is_active: Optional[bool] = None


# Схема для ответа
class PlaceRead(PlaceBase):
    id: int

    model_config = {"from_attributes": True}