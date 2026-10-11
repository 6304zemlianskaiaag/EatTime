# app/services/booking.py
# Сервис Booking — бизнес-логика

from typing import Optional, List
from datetime import datetime

from app.models import Booking, BookingStatus
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate


class BookingService:

    def __init__(self, repo: BookingRepository):
        self.repo = repo

    # Создаёт бронь (проверка конфликта — в crud)
    def create(self, user_id: int, data: BookingCreate) -> Booking:
        if data.end_time <= data.start_time:
            raise ValueError("Время окончания должно быть позже начала")
        return self.repo.create(user_id, data)

    # Возвращает по ID
    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        return self.repo.get_by_id(booking_id)

    # Брони пользователя
    def get_by_user(self, user_id: int) -> List[Booking]:
        return self.repo.get_by_user(user_id)

    # Брони ресторана
    def get_by_restaurant(self, restaurant_id: int) -> List[Booking]:
        return self.repo.get_by_restaurant(restaurant_id)

    # Меняет статус
    def update_status(self, booking_id: int, status_str: str) -> Optional[Booking]:
        try:
            status = BookingStatus(status_str)
        except ValueError:
            raise ValueError(f"Неверный статус: {status_str}")
        return self.repo.update_status(booking_id, status)

    # Отмена брони пользователем
    def cancel(self, booking_id: int, user_id: int) -> bool:
        return self.repo.cancel(booking_id, user_id)

    # Удаляет
    def delete(self, booking_id: int) -> bool:
        return self.repo.delete(booking_id)

    # Поиск альтернативных слотов
    def find_alternative_slots(
        self,
        restaurant_id: int,
        desired_start: datetime,
        desired_end: datetime,
        guests_count: int,
    ):
        return self.repo.find_alternative_slots(
            restaurant_id, desired_start, desired_end, guests_count
        )