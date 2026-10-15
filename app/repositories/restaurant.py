from typing import Optional, List
from sqlalchemy.orm import Session

from app import crud
from app.models import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
class RestaurantRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: RestaurantCreate) -> Restaurant:
        return crud.create_restaurant(
            self.session,
            name=data.name,
            address=data.address,
            opening_time=data.opening_time,
            closing_time=data.closing_time,
            description=data.description,
            phone=data.phone,
            avg_check=data.avg_check,
        )
    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        return crud.get_restaurant_by_id(self.session, restaurant_id)
    def get_all(self) -> List[Restaurant]:
        return crud.get_all_restaurants(self.session)
    def search_by_cuisine(self, cuisine_name: str) -> List[Restaurant]:
        return crud.search_restaurants_by_cuisine(self.session, cuisine_name)
    def update(self, restaurant_id: int, data: RestaurantUpdate) -> Optional[Restaurant]:
        fields = data.model_dump(exclude_unset=True)
        return crud.update_restaurant(self.session, restaurant_id, **fields)
    def delete(self, restaurant_id: int) -> bool:
        return crud.delete_restaurant(self.session, restaurant_id)

    # M:N: привязка кухни
    def attach_cuisine(self, restaurant_id: int, cuisine_id: int) -> None:
        return crud.attach_cuisine_to_restaurant(self.session, restaurant_id, cuisine_id)

    # M:N: отвязка кухни
    def detach_cuisine(self, restaurant_id: int, cuisine_id: int) -> None:
        return crud.detach_cuisine_from_restaurant(self.session, restaurant_id, cuisine_id)

    # M:N: привязка админа
    def attach_admin(self, restaurant_id: int, user_id: int) -> None:
        return crud.attach_admin_to_restaurant(self.session, user_id, restaurant_id)

    # M:N: отвязка админа
    def detach_admin(self, restaurant_id: int, user_id: int) -> None:
        return crud.detach_admin_from_restaurant(self.session, user_id, restaurant_id)