# app/schemas/auth.py
# DTO-схемы для аутентификации

from pydantic import BaseModel

# Схема ответа на логин — JWT-токен
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"