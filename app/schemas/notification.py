# app/schemas/notification.py
# DTO-схемы Pydantic для уведомлений

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Схема для создания
class NotificationCreate(BaseModel):
    user_id: int
    type: str
    payload: Optional[dict] = None


# Схема для ответа
class NotificationRead(BaseModel):
    id: int
    user_id: int
    type: str
    payload: Optional[dict] = None
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}