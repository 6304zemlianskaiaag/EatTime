# app/api/table_types.py
# HTTP-роутер для типов столиков

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import get_table_type_service
from app.services.table_type import TableTypeService
from app.schemas.table_type import TableTypeCreate, TableTypeRead, TableTypeUpdate

router = APIRouter(prefix="/table-types", tags=["table-types"])


# Создаёт тип столика
@router.post("/", response_model=TableTypeRead, status_code=201)
def create_table_type(
    data: TableTypeCreate,
    service: TableTypeService = Depends(get_table_type_service),
):
    return service.create(data)


# Все типы столиков
@router.get("/", response_model=List[TableTypeRead])
def list_table_types(service: TableTypeService = Depends(get_table_type_service)):
    return service.get_all()


# Тип столика по ID
@router.get("/{tt_id}", response_model=TableTypeRead)
def get_table_type(
    tt_id: int,
    service: TableTypeService = Depends(get_table_type_service),
):
    tt = service.get_by_id(tt_id)
    if tt is None:
        raise HTTPException(status_code=404, detail="Тип столика не найден")
    return tt


# Обновляет тип столика
@router.put("/{tt_id}", response_model=TableTypeRead)
def update_table_type(
    tt_id: int,
    data: TableTypeUpdate,
    service: TableTypeService = Depends(get_table_type_service),
):
    fields = data.model_dump(exclude_unset=True)
    tt = service.update(tt_id, **fields)
    if tt is None:
        raise HTTPException(status_code=404, detail="Тип столика не найден")
    return tt


# Удаляет тип столика
@router.delete("/{tt_id}", status_code=204)
def delete_table_type(
    tt_id: int,
    service: TableTypeService = Depends(get_table_type_service),
):
    try:
        if not service.delete(tt_id):
            raise HTTPException(status_code=404, detail="Тип столика не найден")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))