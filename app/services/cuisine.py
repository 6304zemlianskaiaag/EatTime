# app/services/cuisine.py
# Сервис Cuisine — бизнес-логика

from typing import Optional, List

from app.models import Cuisine
from app.repositories.cuisine import CuisineRepository
from app.schemas.cuisine import CuisineCreate


class CuisineService:

    def __init__(self, repo: CuisineRepository):
        self.repo = repo

    def create(self, data: CuisineCreate) -> Cuisine:
        return self.repo.create(data)

    def get_by_id(self, cuisine_id: int) -> Optional[Cuisine]:
        return self.repo.get_by_id(cuisine_id)

    def get_all(self) -> List[Cuisine]:
        return self.repo.get_all()

    def update(self, cuisine_id: int, new_name: str) -> Optional[Cuisine]:
        return self.repo.update(cuisine_id, new_name)

    def delete(self, cuisine_id: int) -> bool:
        return self.repo.delete(cuisine_id)