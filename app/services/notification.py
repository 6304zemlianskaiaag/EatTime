# app/services/notification.py
# Сервис Notification — бизнес-логика

from typing import Optional, List

from app.models import Notification
from app.repositories.notification import NotificationRepository
from app.schemas.notification import NotificationCreate


class NotificationService:

    def __init__(self, repo: NotificationRepository):
        self.repo = repo

    def create(self, data: NotificationCreate) -> Notification:
        return self.repo.create(data)

    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        return self.repo.get_by_id(notification_id)

    def get_by_user(self, user_id: int, only_unread: bool = False) -> List[Notification]:
        return self.repo.get_by_user(user_id, only_unread)

    def mark_read(self, notification_id: int) -> Optional[Notification]:
        return self.repo.mark_read(notification_id)

    def delete(self, notification_id: int) -> bool:
        return self.repo.delete(notification_id)