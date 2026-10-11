# app/api/roles.py
# HTTP-роутер для ролей

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_role_service
from app.services.role import RoleService
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate

router = APIRouter(prefix="/roles", tags=["roles"])


# Создаёт роль
@router.post("/", response_model=RoleRead, status_code=201)
def create_role(
    data: RoleCreate,
    service: RoleService = Depends(get_role_service),
):
    return service.create(data)


# Все роли
@router.get("/", response_model=List[RoleRead])
def list_roles(service: RoleService = Depends(get_role_service)):
    return service.get_all()


# Роль по ID
@router.get("/{role_id}", response_model=RoleRead)
def get_role(
    role_id: int,
    service: RoleService = Depends(get_role_service),
):
    role = service.get_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return role


# Обновляет роль
@router.put("/{role_id}", response_model=RoleRead)
def update_role(
    role_id: int,
    data: RoleUpdate,
    service: RoleService = Depends(get_role_service),
):
    role = service.update(role_id, data.name)
    if role is None:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return role


# Удаляет роль
@router.delete("/{role_id}", status_code=204)
def delete_role(
    role_id: int,
    service: RoleService = Depends(get_role_service),
):
    try:
        if not service.delete(role_id):
            raise HTTPException(status_code=404, detail="Роль не найдена")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))