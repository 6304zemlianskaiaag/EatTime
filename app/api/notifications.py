# app/api/notifications.py
# HTTP-роутер для уведомлений

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_notification_service, get_current_user
from app.services.notification import NotificationService
from app.schemas.notification import NotificationCreate, NotificationRead
from app.models import User

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=NotificationRead, status_code=201)
def create_notification(data: NotificationCreate,
    service: NotificationService = Depends(get_notification_service),
):
    return service.create(data)

@router.get("/", response_model=List[NotificationRead])
def list_my_notifications(
    only_unread: bool = False,
    service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_user),):
    return service.get_by_user(current_user.id, only_unread)

@router.get("/{notification_id}", response_model=NotificationRead)
def get_notification(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service),
):
    notification = service.get_by_id(notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    return notification

@router.patch("/{notification_id}/read", response_model=NotificationRead)
def mark_read(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service),
):
    notification = service.mark_read(notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    return notification

@router.delete("/{notification_id}", status_code=204)
def delete_notification(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service),
):
    if not service.delete(notification_id):
        raise HTTPException(status_code=404, detail="Уведомление не найдено")