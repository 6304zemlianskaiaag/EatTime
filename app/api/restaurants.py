# app/api/restaurants.py
# HTTP-роутер для CRUD-операций над Restaurant

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_restaurant_service
from app.services.restaurant import RestaurantService
from app.schemas.restaurant import RestaurantCreate, RestaurantRead, RestaurantUpdate

from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantRead,
    RestaurantUpdate,
    AttachCuisineRequest,
    AttachAdminRequest,
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=RestaurantRead, status_code=201)
def create_restaurant(
    data: RestaurantCreate,
    service: RestaurantService = Depends(get_restaurant_service),
):
    return service.create(data)

@router.get("/", response_model=List[RestaurantRead])
def list_restaurants(service: RestaurantService = Depends(get_restaurant_service)):
    return service.get_all()


@router.get("/search", response_model=List[RestaurantRead])
def search_restaurants(
    cuisine: str,
    service: RestaurantService = Depends(get_restaurant_service),
):
    return service.search_by_cuisine(cuisine)

@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(
    restaurant_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
):
    restaurant = service.get_by_id(restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Ресторан не найден")
    return restaurant


# Обновляет ресторан по ID
@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    service: RestaurantService = Depends(get_restaurant_service),
):
    restaurant = service.update(restaurant_id, data)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Ресторан не найден")
    return restaurant


# Удаляет ресторан по ID
@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(
    restaurant_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
):
    if not service.delete(restaurant_id):
        raise HTTPException(status_code=404, detail="Ресторан не найден")

# Привязать кухню к ресторану
@router.post("/{restaurant_id}/cuisines", status_code=201)
def attach_cuisine(
    restaurant_id: int,
    data: AttachCuisineRequest,
    service: RestaurantService = Depends(get_restaurant_service),
):
    try:
        service.attach_cuisine(restaurant_id, data.cuisine_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Кухня привязана"}


# Отвязать кухню от ресторана
@router.delete("/{restaurant_id}/cuisines/{cuisine_id}", status_code=204)
def detach_cuisine(
    restaurant_id: int,
    cuisine_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
):
    service.detach_cuisine(restaurant_id, cuisine_id)


# Привязать админа к ресторану
@router.post("/{restaurant_id}/admins", status_code=201)
def attach_admin(
    restaurant_id: int,
    data: AttachAdminRequest,
    service: RestaurantService = Depends(get_restaurant_service),
):
    try:
        service.attach_admin(restaurant_id, data.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Админ привязан"}


# Отвязать админа от ресторана
@router.delete("/{restaurant_id}/admins/{user_id}", status_code=204)
def detach_admin(
    restaurant_id: int,
    user_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
):
    service.detach_admin(restaurant_id, user_id)

