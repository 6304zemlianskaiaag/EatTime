# app/schemas/role.py
# DTO-схемы Pydantic для роли

from pydantic import BaseModel


# Общие поля
class RoleBase(BaseModel):
    code: str
    name: str


# Схема для создания
class RoleCreate(RoleBase):
    pass


# Схема для обновления
class RoleUpdate(BaseModel):
    name: str


# Схема для ответа
class RoleRead(RoleBase):
    id: int

    model_config = {"from_attributes": True}