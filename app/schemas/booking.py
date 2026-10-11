# app/schemas/booking.py
# DTO-схемы Pydantic для брони

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Общие поля
class BookingBase(BaseModel):
    place_id: int
    start_time: datetime
    end_time: datetime
    guests_count: int = Field(gt=0)
    comment: Optional[str] = None


# Схема для создания
class BookingCreate(BookingBase):
    pass


# Схема для обновления — только комментарий
class BookingUpdate(BaseModel):
    comment: Optional[str] = None


# Схема для смены статуса
class BookingStatusUpdate(BaseModel):
    status: str


# Схема для ответа
class BookingRead(BookingBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}