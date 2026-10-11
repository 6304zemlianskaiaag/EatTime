# app/repositories/place.py
# Репозиторий Place — обёртка над crud.py

from typing import Optional, List
from sqlalchemy.orm import Session

from app import crud
from app.models import Place
from app.schemas.place import PlaceCreate, PlaceUpdate


class PlaceRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: PlaceCreate) -> Place:
        return crud.create_place(
            self.session,
            table_type_id=data.type_table_id,
            restaurant_id=data.restaurant_id,
            is_active=data.is_active,
        )

    def get_by_id(self, place_id: int) -> Optional[Place]:
        return crud.get_place(self.session, place_id)

    def get_by_restaurant(self, restaurant_id: int, only_active: bool = True) -> List[Place]:
        return crud.get_places_by_restaurant(self.session, restaurant_id, only_active)

    def update(self, place_id: int, data: PlaceUpdate) -> Optional[Place]:
        fields = data.model_dump(exclude_unset=True)
        return crud.update_place(self.session, place_id, **fields)

    def delete(self, place_id: int) -> bool:
        return crud.delete_place(self.session, place_id)