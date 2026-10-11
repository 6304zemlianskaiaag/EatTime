# app/api/bookings.py
# HTTP-роутер для бронирований

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime

from app.dependencies import get_booking_service, get_current_user
from app.services.booking import BookingService
from app.schemas.booking import BookingCreate, BookingRead, BookingStatusUpdate
from app.models import User

router = APIRouter(prefix="/bookings", tags=["bookings"])


# Создаёт бронь (только для авторизованных)
@router.post("/", response_model=BookingRead, status_code=201)
def create_booking(
    data: BookingCreate,
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.create(current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Возвращает брони текущего пользователя
@router.get("/", response_model=List[BookingRead])
def list_my_bookings(
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_user(current_user.id)


# Альтернативные слоты — ДО /{booking_id}
@router.get("/alternatives/{restaurant_id}")
def find_alternatives(
    restaurant_id: int,
    start: datetime,
    end: datetime,
    guests: int,
    service: BookingService = Depends(get_booking_service),
):
    slots = service.find_alternative_slots(restaurant_id, start, end, guests)
    return [
        {
            "place_id": place.id,
            "seats": place.table_type.seats,
            "start": s,
            "end": e,
        }
        for place, s, e in slots
    ]


# Брони ресторана — ДО /{booking_id}
@router.get("/restaurant/{restaurant_id}", response_model=List[BookingRead])
def list_restaurant_bookings(
    restaurant_id: int,
    service: BookingService = Depends(get_booking_service),
):
    return service.get_by_restaurant(restaurant_id)


# Отмена брони текущим пользователем
@router.post("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    if not service.cancel(booking_id, current_user.id):
        raise HTTPException(status_code=400, detail="Не удалось отменить бронь")
    return {"message": "Бронь отменена"}


# Смена статуса (для админа)
@router.patch("/{booking_id}/status", response_model=BookingRead)
def update_status(
    booking_id: int,
    data: BookingStatusUpdate,
    service: BookingService = Depends(get_booking_service),
):
    try:
        booking = service.update_status(booking_id, data.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if booking is None:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    return booking


# Возвращает бронь по ID
@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
):
    booking = service.get_by_id(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    return booking


# Удаляет бронь (для админа)
@router.delete("/{booking_id}", status_code=204)
def delete_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
):
    if not service.delete(booking_id):
        raise HTTPException(status_code=404, detail="Бронь не найдена")