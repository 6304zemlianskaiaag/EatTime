# app/services/restaurant.py
# Сервис Restaurant — бизнес-логика

from typing import Optional, List

from app.models import Restaurant
from app.repositories.restaurant import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:

    def __init__(self, repo: RestaurantRepository):
        self.repo = repo

    # Создаёт ресторан
    def create(self, data: RestaurantCreate) -> Restaurant:
        return self.repo.create(data)

    # Возвращает по ID
    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        return self.repo.get_by_id(restaurant_id)

    # Возвращает все
    def get_all(self) -> List[Restaurant]:
        return self.repo.get_all()

    # Поиск по кухне
    def search_by_cuisine(self, cuisine_name: str) -> List[Restaurant]:
        return self.repo.search_by_cuisine(cuisine_name)

    # Обновляет
    def update(self, restaurant_id: int, data: RestaurantUpdate) -> Optional[Restaurant]:
        return self.repo.update(restaurant_id, data)

    # Удаляет
    def delete(self, restaurant_id: int) -> bool:
        return self.repo.delete(restaurant_id)

    # M:N: привязка кухни
    def attach_cuisine(self, restaurant_id: int, cuisine_id: int) -> None:
        return self.repo.attach_cuisine(restaurant_id, cuisine_id)

    # M:N: отвязка кухни
    def detach_cuisine(self, restaurant_id: int, cuisine_id: int) -> None:
        return self.repo.detach_cuisine(restaurant_id, cuisine_id)

    # M:N: привязка админа
    def attach_admin(self, restaurant_id: int, user_id: int) -> None:
        return self.repo.attach_admin(restaurant_id, user_id)

    # M:N: отвязка админа
    def detach_admin(self, restaurant_id: int, user_id: int) -> None:
        return self.repo.detach_admin(restaurant_id, user_id)