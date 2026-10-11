# app/schemas/user.py
# DTO-схемы Pydantic для пользователя

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# Общие поля для всех схем User
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None


# Схема для регистрации — содержит пароль
class UserCreate(UserBase):
    password: str = Field(min_length=8)
    role_id: int


# Схема для обновления — все поля опциональны
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None


# Схема для ответа клиенту — без пароля
class UserRead(UserBase):
    id: int
    is_active: bool
    role_id: int

    model_config = {"from_attributes": True}