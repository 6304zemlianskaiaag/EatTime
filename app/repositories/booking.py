# app/repositories/booking.py
# Репозиторий Booking — обёртка над crud.py

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from app import crud
from app.models import Booking, BookingStatus
from app.schemas.booking import BookingCreate


class BookingRepository:

    def __init__(self, session: Session):
        self.session = session

    # Создаёт бронь (crud сам проверяет конфликт)
    def create(self, user_id: int, data: BookingCreate) -> Booking:
        return crud.create_booking(
            self.session,
            user_id=user_id,
            place_id=data.place_id,
            start_time=data.start_time,
            end_time=data.end_time,
            guests_count=data.guests_count,
            comment=data.comment,
        )

    # Возвращает по ID
    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        return crud.get_booking(self.session, booking_id)

    # Брони пользователя
    def get_by_user(self, user_id: int) -> List[Booking]:
        return crud.get_bookings_by_user(self.session, user_id)

    # Брони ресторана
    def get_by_restaurant(self, restaurant_id: int) -> List[Booking]:
        return crud.get_bookings_by_restaurant(self.session, restaurant_id)

    # Смена статуса
    def update_status(self, booking_id: int, status: BookingStatus) -> Optional[Booking]:
        return crud.update_booking_status(self.session, booking_id, status)

    # Отмена брони пользователем
    def cancel(self, booking_id: int, user_id: int) -> bool:
        return crud.cancel_booking(self.session, booking_id, user_id)

    # Удаляет
    def delete(self, booking_id: int) -> bool:
        return crud.delete_booking(self.session, booking_id)

    # Поиск альтернативных слотов
    def find_alternative_slots(
        self,
        restaurant_id: int,
        desired_start: datetime,
        desired_end: datetime,
        guests_count: int,
    ):
        return crud.find_alternative_slots(
            self.session,
            restaurant_id,
            desired_start,
            desired_end,
            guests_count,
        )