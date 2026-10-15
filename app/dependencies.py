from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.db import SessionLocal
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.security import decode_token
from app.models import User

from app.repositories.restaurant import RestaurantRepository
from app.services.restaurant import RestaurantService

from app.repositories.booking import BookingRepository
from app.services.booking import BookingService

from app.repositories.cuisine import CuisineRepository
from app.services.cuisine import CuisineService

from app.repositories.notification import NotificationRepository
from app.services.notification import NotificationService

from app.repositories.place import PlaceRepository
from app.services.place import PlaceService


from app.repositories.table_type import TableTypeRepository
from app.services.table_type import TableTypeService

from app.repositories.role import RoleRepository
from app.services.role import RoleService

def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
def get_user_repository(session: Session = Depends(get_session),) -> UserRepository:
    return UserRepository(session)
def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") #  откуда брать токен

def get_current_user(token: str = Depends(oauth2_scheme), service: UserService = Depends(get_user_service),) -> User:
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
        )
    user = service.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )
    return user

def get_restaurant_repository(session: Session = Depends(get_session),) -> RestaurantRepository:
    return RestaurantRepository(session)
def get_restaurant_service(repo: RestaurantRepository = Depends(get_restaurant_repository),) -> RestaurantService:
    return RestaurantService(repo)

def get_booking_repository(session: Session = Depends(get_session),) -> BookingRepository:
    return BookingRepository(session)
def get_booking_service(repo: BookingRepository = Depends(get_booking_repository),) -> BookingService:
    return BookingService(repo)
def get_cuisine_repository(session: Session = Depends(get_session),) -> CuisineRepository:
    return CuisineRepository(session)
def get_cuisine_service(repo: CuisineRepository = Depends(get_cuisine_repository),) -> CuisineService:
    return CuisineService(repo)
def get_notification_repository(session: Session = Depends(get_session),) -> NotificationRepository:
    return NotificationRepository(session)
def get_notification_service( repo: NotificationRepository = Depends(get_notification_repository),) -> NotificationService:
    return NotificationService(repo)

def get_place_repository(session: Session = Depends(get_session),) -> PlaceRepository:
    return PlaceRepository(session)
def get_place_service(repo: PlaceRepository = Depends(get_place_repository),) -> PlaceService:
    return PlaceService(repo)

def get_table_type_repository(session: Session = Depends(get_session),) -> TableTypeRepository:
    return TableTypeRepository(session)
def get_table_type_service(repo: TableTypeRepository = Depends(get_table_type_repository),) -> TableTypeService:
    return TableTypeService(repo)
def get_role_repository(session: Session = Depends(get_session),) -> RoleRepository:
    return RoleRepository(session)
def get_role_service(repo: RoleRepository = Depends(get_role_repository),) -> RoleService:
    return RoleService(repo)