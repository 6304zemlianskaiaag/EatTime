# app/schemas/restaurant.py
# DTO-схемы Pydantic для ресторана

from typing import Optional
from datetime import time
from decimal import Decimal
from pydantic import BaseModel


# Общие поля для всех схем Restaurant
class RestaurantBase(BaseModel):
    name: str
    address: str
    description: Optional[str] = None
    phone: Optional[str] = None
    opening_time: time
    closing_time: time
    avg_check: Optional[Decimal] = None


# Схема для создания
class RestaurantCreate(RestaurantBase):
    pass


# Схема для обновления — все поля опциональны
class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    avg_check: Optional[Decimal] = None


# Схема для ответа
class RestaurantRead(RestaurantBase):
    id: int
    status: str

    model_config = {"from_attributes": True}

# Схема для привязки кухни к ресторану
class AttachCuisineRequest(BaseModel):
    cuisine_id: int


# Схема для привязки админа к ресторану
class AttachAdminRequest(BaseModel):
    user_id: int