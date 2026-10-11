# app/schemas/cuisine.py
# DTO-схемы Pydantic для кухни

from pydantic import BaseModel


# Общие поля
class CuisineBase(BaseModel):
    name: str


# Схема для создания
class CuisineCreate(CuisineBase):
    pass


# Схема для обновления
class CuisineUpdate(BaseModel):
    name: str


# Схема для ответа
class CuisineRead(CuisineBase):
    id: int

    model_config = {"from_attributes": True}