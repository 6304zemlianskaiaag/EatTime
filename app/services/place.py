# app/services/place.py
# Сервис Place — бизнес-логика

from typing import Optional, List

from app.models import Place
from app.repositories.place import PlaceRepository
from app.schemas.place import PlaceCreate, PlaceUpdate


class PlaceService:

    def __init__(self, repo: PlaceRepository):
        self.repo = repo

    def create(self, data: PlaceCreate) -> Place:
        return self.repo.create(data)

    def get_by_id(self, place_id: int) -> Optional[Place]:
        return self.repo.get_by_id(place_id)

    def get_by_restaurant(self, restaurant_id: int, only_active: bool = True) -> List[Place]:
        return self.repo.get_by_restaurant(restaurant_id, only_active)

    def update(self, place_id: int, data: PlaceUpdate) -> Optional[Place]:
        return self.repo.update(place_id, data)

    def delete(self, place_id: int) -> bool:
        return self.repo.delete(place_id)