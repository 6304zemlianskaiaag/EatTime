# app/api/users.py
# HTTP-роутер для CRUD-операций над User

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_user_service, get_current_user
from app.services.user import UserService
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


# Создаёт нового пользователя (регистрация)
@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Возвращает список всех пользователей
@router.get("/", response_model=List[UserRead])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all()


# Возвращает текущего пользователя по токену (ЗАЩИЩЁННЫЙ)
@router.get("/me", response_model=UserRead)
def get_me(current_user = Depends(get_current_user)):
    return current_user


# Возвращает пользователя по ID
@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


# Обновляет пользователя по ID
@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    user = service.update(user_id, data)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


# Удаляет пользователя по ID
@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    if not service.delete(user_id):
        raise HTTPException(status_code=404, detail="Пользователь не найден")