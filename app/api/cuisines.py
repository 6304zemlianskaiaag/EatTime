# app/api/cuisines.py
# HTTP-роутер для кухонь

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_cuisine_service
from app.services.cuisine import CuisineService
from app.schemas.cuisine import CuisineCreate, CuisineRead, CuisineUpdate

router = APIRouter(prefix="/cuisines", tags=["cuisines"])


# Создаёт кухню
@router.post("/", response_model=CuisineRead, status_code=201)
def create_cuisine(
    data: CuisineCreate,
    service: CuisineService = Depends(get_cuisine_service),
):
    return service.create(data)


# Возвращает все кухни
@router.get("/", response_model=List[CuisineRead])
def list_cuisines(service: CuisineService = Depends(get_cuisine_service)):
    return service.get_all()


# Возвращает кухню по ID
@router.get("/{cuisine_id}", response_model=CuisineRead)
def get_cuisine(
    cuisine_id: int,
    service: CuisineService = Depends(get_cuisine_service),
):
    cuisine = service.get_by_id(cuisine_id)
    if cuisine is None:
        raise HTTPException(status_code=404, detail="Кухня не найдена")
    return cuisine


# Обновляет кухню
@router.put("/{cuisine_id}", response_model=CuisineRead)
def update_cuisine(
    cuisine_id: int,
    data: CuisineUpdate,
    service: CuisineService = Depends(get_cuisine_service),
):
    cuisine = service.update(cuisine_id, data.name)
    if cuisine is None:
        raise HTTPException(status_code=404, detail="Кухня не найдена")
    return cuisine


# Удаляет кухню
@router.delete("/{cuisine_id}", status_code=204)
def delete_cuisine(
    cuisine_id: int,
    service: CuisineService = Depends(get_cuisine_service),
):
    try:
        if not service.delete(cuisine_id):
            raise HTTPException(status_code=404, detail="Кухня не найдена")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))