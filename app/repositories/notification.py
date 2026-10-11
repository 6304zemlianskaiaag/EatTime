# app/repositories/notification.py
# Репозиторий Notification — обёртка над crud.py

from typing import Optional, List
from sqlalchemy.orm import Session

from app import crud
from app.models import Notification, NotificationType
from app.schemas.notification import NotificationCreate


class NotificationRepository:

    def __init__(self, session: Session):
        self.session = session

    # Создаёт уведомление
    def create(self, data: NotificationCreate) -> Notification:
        return crud.create_notification(
            self.session,
            user_id=data.user_id,
            type_=NotificationType(data.type),
            payload=data.payload,
        )

    # Возвращает по ID
    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        return crud.get_notification(self.session, notification_id)

    # Уведомления пользователя
    def get_by_user(self, user_id: int, only_unread: bool = False) -> List[Notification]:
        return crud.get_notifications_by_user(self.session, user_id, only_unread)

    # Отметить прочитанным
    def mark_read(self, notification_id: int) -> Optional[Notification]:
        return crud.mark_notification_read(self.session, notification_id)

    # Удаляет
    def delete(self, notification_id: int) -> bool:
        return crud.delete_notification(self.session, notification_id)