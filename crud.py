from datetime import datetime, time
from decimal import Decimal
from typing import Optional, List, Tuple, Dict, Any

from sqlalchemy import select, and_
from sqlalchemy.orm import Session, selectinload, joinedload
from models import ( Role, User, Restaurant, Cuisine, TableType,Place, RestaurantStatus, TableLocation,
                     Booking, BookingStatus, Notification, NotificationType,)
def create_role(session: Session, code: str, name: str) -> Role:
    role = Role(code=code, name=name)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role
def get_role_by_code(session: Session, code: str) -> Optional[Role]:
    return session.scalar(select(Role).where(Role.code == code))
def get_all_roles(session: Session) -> List[Role]:
    return list(session.scalars(select(Role)))
def update_role(session: Session, role_id: int, new_name: str) -> Optional[Role]:
    role = session.get(Role, role_id)
    if role is None:
        return None
    role.name = new_name
    session.commit()
    session.refresh(role)
    return role
def delete_role(session: Session, role_id: int) -> bool:
    role = session.get(Role, role_id)
    if role is None:
        return False
    if role.users:
        raise ValueError("Нельзя удалить роль, у которой есть пользователи")
    session.delete(role)
    session.commit()
    return True
def create_user(session: Session, email: str, password_hash: str,full_name: str, role_id: int, phone: Optional[str] = None) -> User:
    user = User(
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        role_id=role_id,
        phone=phone,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)
def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.scalar(select(User).where(User.email == email))

def get_all_users(session: Session) -> List[User]:
    return list(session.scalars(select(User)))
def update_user(session: Session, user_id: int, **fields) -> Optional[User]:
    user = session.get(User, user_id)
    if user is None:
        return None
    for key, value in fields.items():
        if hasattr(user, key):
            setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user
def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if user is None:
        return False
    session.delete(user)
    session.commit()
    return True
def create_cuisine(session: Session, name: str) -> Cuisine:
    cuisine = Cuisine(name=name)
    session.add(cuisine)
    session.commit()
    session.refresh(cuisine)
    return cuisine
def get_cuisine_by_id(session: Session, cuisine_id: int) -> Optional[Cuisine]:
    return session.get(Cuisine, cuisine_id)
def get_all_cuisines(session: Session) -> List[Cuisine]:
    return list(session.scalars(select(Cuisine)))
def update_cuisine(session: Session, cuisine_id: int, new_name: str) -> Optional[Cuisine]:
    cuisine = session.get(Cuisine, cuisine_id)
    if cuisine is None:
        return None
    cuisine.name = new_name
    session.commit()
    session.refresh(cuisine)
    return cuisine
def delete_cuisine(session: Session, cuisine_id: int) -> bool:
    cuisine = session.get(Cuisine, cuisine_id)
    if cuisine is None:
        return False
    if cuisine.restaurants:
        raise ValueError("Нельзя удалить кухню, привязанную к ресторанам")
    session.delete(cuisine)
    session.commit()
    return True
def create_restaurant(session: Session, name: str, address: str,
                      opening_time: time, closing_time: time,
                      description: Optional[str] = None,
                      phone: Optional[str] = None,
                      avg_check: Optional[Decimal] = None,
                      status: RestaurantStatus = RestaurantStatus.pending) -> Restaurant:
    restaurant = Restaurant(
        name=name,
        address=address,
        opening_time=opening_time,
        closing_time=closing_time,
        description=description,
        phone=phone,
        avg_check=avg_check,
        status=status,
    )
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant
def get_restaurant_by_id(session: Session, restaurant_id: int) -> Optional[Restaurant]:
    return session.scalar(
        select(Restaurant)
        .options(
            selectinload(Restaurant.cuisines),
            selectinload(Restaurant.places),
            selectinload(Restaurant.admins),
        )
        .where(Restaurant.id == restaurant_id)
    )
def get_all_restaurants(session: Session) -> List[Restaurant]:
    return list(session.scalars(select(Restaurant)))
def search_restaurants_by_cuisine(session: Session, cuisine_name: str) -> List[Restaurant]:
    stmt = (
        select(Restaurant)
        .join(Restaurant.cuisines)
        .where(Cuisine.name == cuisine_name)
    )
    return list(session.scalars(stmt))
def update_restaurant(session: Session, restaurant_id: int, **fields) -> Optional[Restaurant]:
    restaurant = session.get(Restaurant, restaurant_id)
    if restaurant is None:
        return None
    for key, value in fields.items():
        if hasattr(restaurant, key):
            setattr(restaurant, key, value)
    session.commit()
    session.refresh(restaurant)
    return restaurant

def delete_restaurant(session: Session, restaurant_id: int) -> bool:
    restaurant = session.get(Restaurant, restaurant_id)
    if restaurant is None:
        return False
    session.delete(restaurant)
    session.commit()
    return True
def create_table_type(session: Session, seats: int,
                      location: TableLocation) -> TableType:
    tt = TableType(seats=seats, location=location)
    session.add(tt)
    session.commit()
    session.refresh(tt)
    return tt
def get_table_type(session: Session, tt_id: int) -> Optional[TableType]:
    return session.get(TableType, tt_id)
def get_all_table_types(session: Session) -> List[TableType]:
    return list(session.scalars(select(TableType)))
def update_table_type(session: Session, tt_id: int, **fields) -> Optional[TableType]:
    tt = session.get(TableType, tt_id)
    if tt is None:
        return None
    for key, value in fields.items():
        if hasattr(tt, key):
            setattr(tt, key, value)
    session.commit()
    session.refresh(tt)
    return tt
def delete_table_type(session: Session, tt_id: int) -> bool:
    tt = session.get(TableType, tt_id)
    if tt is None:
        return False
    if tt.places:
        raise ValueError("Нельзя удалить тип столика, у которого есть столики")
    session.delete(tt)
    session.commit()
    return True
def attach_cuisine_to_restaurant(session: Session,
                                 restaurant_id: int,
                                 cuisine_id: int) -> None:
    restaurant = session.get(Restaurant, restaurant_id)
    cuisine = session.get(Cuisine, cuisine_id)
    if restaurant is None or cuisine is None:
        raise ValueError("Ресторан или кухня не найдены")
    if cuisine not in restaurant.cuisines:
        restaurant.cuisines.append(cuisine)
        session.commit()
def detach_cuisine_from_restaurant(session: Session,
                                   restaurant_id: int,
                                   cuisine_id: int) -> None:
    restaurant = session.get(Restaurant, restaurant_id)
    if restaurant is None:
        return
    cuisine = session.get(Cuisine, cuisine_id)
    if cuisine and cuisine in restaurant.cuisines:
        restaurant.cuisines.remove(cuisine)
        session.commit()
def attach_admin_to_restaurant(session: Session,
                               user_id: int,
                               restaurant_id: int) -> None:
    user = session.get(User, user_id)
    restaurant = session.get(Restaurant, restaurant_id)
    if user is None or restaurant is None:
        raise ValueError("Пользователь или ресторан не найдены")
    if restaurant not in user.restaurants:
        user.restaurants.append(restaurant)
        session.commit()

def detach_admin_from_restaurant(session: Session,
                                 user_id: int,
                                 restaurant_id: int) -> None:
    user = session.get(User, user_id)
    if user is None:
        return
    restaurant = session.get(Restaurant, restaurant_id)
    if restaurant and restaurant in user.restaurants:
        user.restaurants.remove(restaurant)
        session.commit()
def create_place(session: Session, table_type_id: int,
                 restaurant_id: int, is_active: bool = True) -> Place:
    place = Place(
        type_table_id=table_type_id,
        restaurant_id=restaurant_id,
        is_active=is_active,
    )
    session.add(place)
    session.commit()
    session.refresh(place)
    return place
def get_place(session: Session, place_id: int) -> Optional[Place]:
    return session.get(Place, place_id)
def get_places_by_restaurant(session: Session,
                             restaurant_id: int,
                             only_active: bool = True) -> List[Place]:
    stmt = select(Place).where(Place.restaurant_id == restaurant_id)
    if only_active:
        stmt = stmt.where(Place.is_active.is_(True))
    return list(session.scalars(stmt))
def update_place(session: Session, place_id: int, **fields) -> Optional[Place]:
    place = session.get(Place, place_id)
    if place is None:
        return None
    for key, value in fields.items():
        if hasattr(place, key):
            setattr(place, key, value)
    session.commit()
    session.refresh(place)
    return place
def delete_place(session: Session, place_id: int) -> bool:
    place = session.get(Place, place_id)
    if place is None:
        return False
    if place.bookings:
        place.is_active = False
        session.commit()
        return True
    session.delete(place)
    session.commit()
    return True
def create_booking(session: Session, user_id: int, place_id: int,
                   start_time: datetime, end_time: datetime,
                   guests_count: int, comment: Optional[str] = None) -> Booking:
    conflict = session.scalar(
        select(Booking).where(
            Booking.place_id == place_id,
            Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
            and_(Booking.start_time < end_time, Booking.end_time > start_time),
        )
    )
    if conflict is not None:
        raise ValueError("Столик уже забронирован на это время")

    booking = Booking(
        user_id=user_id,
        place_id=place_id,
        start_time=start_time,
        end_time=end_time,
        guests_count=guests_count,
        comment=comment,
        status=BookingStatus.pending,
    )
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking
def get_booking(session: Session, booking_id: int) -> Optional[Booking]:
    return session.scalar(
        select(Booking)
        .options(
            joinedload(Booking.user),
            joinedload(Booking.place).joinedload(Place.restaurant),
        )
        .where(Booking.id == booking_id)
    )
def get_bookings_by_user(session: Session, user_id: int) -> List[Booking]:
    stmt = (
        select(Booking)
        .options(joinedload(Booking.place).joinedload(Place.restaurant))
        .where(Booking.user_id == user_id)
        .order_by(Booking.start_time.desc())
    )
    return list(session.scalars(stmt))
def get_bookings_by_restaurant(session: Session, restaurant_id: int,
                               status: Optional[BookingStatus] = None) -> List[Booking]:
    stmt = (
        select(Booking)
        .join(Booking.place)
        .options(joinedload(Booking.user))
        .where(Place.restaurant_id == restaurant_id)
        .order_by(Booking.start_time)
    )
    if status is not None:
        stmt = stmt.where(Booking.status == status)
    return list(session.scalars(stmt))
def update_booking_status(session: Session, booking_id: int,
                          status: BookingStatus) -> Optional[Booking]:
    booking = session.get(Booking, booking_id)
    if booking is None:
        return None
    booking.status = status
    session.commit()
    session.refresh(booking)
    return booking
def cancel_booking(session: Session, booking_id: int, user_id: int) -> bool:
    booking = session.get(Booking, booking_id)
    if booking is None or booking.user_id != user_id:
        return False
    if booking.status not in (BookingStatus.pending, BookingStatus.confirmed):
        return False
    booking.status = BookingStatus.cancelled
    session.commit()
    return True
def delete_booking(session: Session, booking_id: int) -> bool:
    booking = session.get(Booking, booking_id)
    if booking is None:
        return False
    session.delete(booking)
    session.commit()
    return True
def find_alternative_slots(session: Session, restaurant_id: int,
                           desired_start: datetime,
                           desired_end: datetime,
                           guests_count: int) -> List[Tuple[Place, datetime, datetime]]:
    from models import TableType

    places = session.scalars(
        select(Place)
        .join(Place.table_type)
        .where(
            Place.restaurant_id == restaurant_id,
            Place.is_active.is_(True),
            TableType.seats >= guests_count,
        )
    ).all()

    result = []
    for place in places:
        conflict = session.scalar(
            select(Booking).where(
                Booking.place_id == place.id,
                Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
                and_(
                    Booking.start_time < desired_end,
                    Booking.end_time > desired_start,
                ),
            )
        )
        if conflict is None:
            result.append((place, desired_start, desired_end))
    return result
def create_notification(session: Session, user_id: int,
                        type_: NotificationType,
                        payload: Optional[Dict[str, Any]] = None) -> Notification:
    notification = Notification(
        user_id=user_id,
        type=type_,
        payload=payload,
    )
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification
def get_notification(session: Session, notification_id: int) -> Optional[Notification]:
    return session.get(Notification, notification_id)
def get_notifications_by_user(session: Session, user_id: int,
                              only_unread: bool = False) -> List[Notification]:
    stmt = select(Notification).where(Notification.user_id == user_id)
    if only_unread:
        stmt = stmt.where(Notification.is_read.is_(False))
    stmt = stmt.order_by(Notification.created_at.desc())
    return list(session.scalars(stmt))
def mark_notification_read(session: Session, notification_id: int) -> Optional[Notification]:
    notification = session.get(Notification, notification_id)
    if notification is None:
        return None
    notification.is_read = True
    session.commit()
    session.refresh(notification)
    return notification
def delete_notification(session: Session, notification_id: int) -> bool:
    notification = session.get(Notification, notification_id)
    if notification is None:
        return False
    session.delete(notification)
    session.commit()
    return True
