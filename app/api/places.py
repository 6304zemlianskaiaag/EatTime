# app/api/places.py
# HTTP-роутер для столиков

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_place_service
from app.services.place import PlaceService
from app.schemas.place import PlaceCreate, PlaceRead, PlaceUpdate

router = APIRouter(prefix="/places", tags=["places"])


# Создаёт столик
@router.post("/", response_model=PlaceRead, status_code=201)
def create_place(
    data: PlaceCreate,
    service: PlaceService = Depends(get_place_service),
):
    return service.create(data)


# Столики ресторана — ДО /{place_id}
@router.get("/restaurant/{restaurant_id}", response_model=List[PlaceRead])
def list_by_restaurant(
    restaurant_id: int,
    only_active: bool = True,
    service: PlaceService = Depends(get_place_service),
):
    return service.get_by_restaurant(restaurant_id, only_active)


# Столик по ID
@router.get("/{place_id}", response_model=PlaceRead)
def get_place(
    place_id: int,
    service: PlaceService = Depends(get_place_service),
):
    place = service.get_by_id(place_id)
    if place is None:
        raise HTTPException(status_code=404, detail="Столик не найден")
    return place


# Обновляет столик
@router.put("/{place_id}", response_model=PlaceRead)
def update_place(
    place_id: int,
    data: PlaceUpdate,
    service: PlaceService = Depends(get_place_service),
):
    place = service.update(place_id, data)
    if place is None:
        raise HTTPException(status_code=404, detail="Столик не найден")
    return place


# Удаляет столик
@router.delete("/{place_id}", status_code=204)
def delete_place(
    place_id: int,
    service: PlaceService = Depends(get_place_service),
):
    if not service.delete(place_id):
        raise HTTPException(status_code=404, detail="Столик не найден")