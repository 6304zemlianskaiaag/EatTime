# app/repositories/cuisine.py
# Репозиторий Cuisine — обёртка над crud.py

from typing import Optional, List
from sqlalchemy.orm import Session

from app import crud
from app.models import Cuisine
from app.schemas.cuisine import CuisineCreate


class CuisineRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: CuisineCreate) -> Cuisine:
        return crud.create_cuisine(self.session, name=data.name)

    def get_by_id(self, cuisine_id: int) -> Optional[Cuisine]:
        return crud.get_cuisine_by_id(self.session, cuisine_id)

    def get_all(self) -> List[Cuisine]:
        return crud.get_all_cuisines(self.session)

    def update(self, cuisine_id: int, new_name: str) -> Optional[Cuisine]:
        return crud.update_cuisine(self.session, cuisine_id, new_name)

    def delete(self, cuisine_id: int) -> bool:
        return crud.delete_cuisine(self.session, cuisine_id)