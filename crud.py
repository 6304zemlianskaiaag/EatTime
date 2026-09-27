# crud.py
from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import (
    Role, User, Cuisine, Restaurant, DiningTable,
    Seats, Booking, Review, Notification
)


# ============ ROLE ============

def create_role(session: Session, code: str, name: str) -> Role:
    role = Role(code=code, name=name)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


def get_role_by_code(session: Session, code: str) -> Optional[Role]:
    return session.scalar(select(Role).where(Role.code == code))


def get_all_roles(session: Session) -> List[Role]:
    return list(session.scalars(select(Role)).all())


# ============ USER ============

def create_user(session: Session, email: str, password_hash: str,
                full_name: str, role_id: int,
                phone: Optional[str] = None) -> User:
    user = User(
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        phone=phone,
        role_id=role_id,
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
    return list(session.scalars(select(User)).all())


def update_user(session: Session, user_id: int, **fields) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None
    for key, value in fields.items():
        if hasattr(user, key):
            setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True


# ============ CUISINE ============

def create_cuisine(session: Session, name: str) -> Cuisine:
    cuisine = Cuisine(name=name)
    session.add(cuisine)
    session.commit()
    session.refresh(cuisine)
    return cuisine


def get_cuisine_by_id(session: Session, cuisine_id: int) -> Optional[Cuisine]:
    return session.get(Cuisine, cuisine_id)


def get_all_cuisines(session: Session) -> List[Cuisine]:
    return list(session.scalars(select(Cuisine)).all())


def update_cuisine(session: Session, cuisine_id: int, name: str) -> Optional[Cuisine]:
    cuisine = session.get(Cuisine, cuisine_id)
    if not cuisine:
        return None
    cuisine.name = name
    session.commit()
    session.refresh(cuisine)
    return cuisine


def delete_cuisine(session: Session, cuisine_id: int) -> bool:
    cuisine = session.get(Cuisine, cuisine_id)
    if not cuisine:
        return False
    session.delete(cuisine)
    session.commit()
    return True


# ============ RESTAURANT ============

def create_restaurant(session: Session, name: str, address: str,
                      opening_time, closing_time,
                      description: Optional[str] = None,
                      phone: Optional[str] = None,
                      avg_check=None,
                      status: str = "pending",
                      cuisine_ids: Optional[List[int]] = None) -> Restaurant:
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
    if cuisine_ids:
        cuisines = list(session.scalars(
            select(Cuisine).where(Cuisine.id.in_(cuisine_ids))
        ).all())
        restaurant.cuisines = cuisines
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant


def get_restaurant_by_id(session: Session, restaurant_id: int) -> Optional[Restaurant]:
    return session.get(Restaurant, restaurant_id)


def get_all_restaurants(session: Session) -> List[Restaurant]:
    return list(session.scalars(select(Restaurant)).all())


def update_restaurant(session: Session, restaurant_id: int, **fields) -> Optional[Restaurant]:
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        return None
    for key, value in fields.items():
        if hasattr(restaurant, key):
            setattr(restaurant, key, value)
    session.commit()
    session.refresh(restaurant)
    return restaurant


def delete_restaurant(session: Session, restaurant_id: int) -> bool:
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        return False
    session.delete(restaurant)
    session.commit()
    return True


# ============ DINING TABLE ============

def create_table(session: Session, seats: int, restaurant_id: int,
                 location: Optional[str] = None) -> DiningTable:
    table = DiningTable(seats=seats, location=location, restaurant_id=restaurant_id)
    session.add(table)
    session.commit()
    session.refresh(table)
    return table


def get_table_by_id(session: Session, table_id: int) -> Optional[DiningTable]:
    return session.get(DiningTable, table_id)


def get_tables_by_restaurant(session: Session, restaurant_id: int) -> List[DiningTable]:
    return list(session.scalars(
        select(DiningTable).where(DiningTable.restaurant_id == restaurant_id)
    ).all())


def update_table(session: Session, table_id: int, **fields) -> Optional[DiningTable]:
    table = session.get(DiningTable, table_id)
    if not table:
        return None
    for key, value in fields.items():
        if hasattr(table, key):
            setattr(table, key, value)
    session.commit()
    session.refresh(table)
    return table


def delete_table(session: Session, table_id: int) -> bool:
    table = session.get(DiningTable, table_id)
    if not table:
        return False
    session.delete(table)
    session.commit()
    return True


# ============ SEATS ============

def create_seats(session: Session, seats_id: int, table_id: int,
                 restaurant_id: int) -> Seats:
    seats = Seats(seats_id=seats_id, table_id=table_id, restaurant_id=restaurant_id)
    session.add(seats)
    session.commit()
    session.refresh(seats)
    return seats


def get_seats_by_id(session: Session, seats_id: int) -> Optional[Seats]:
    return session.get(Seats, seats_id)


def get_seats_by_restaurant(session: Session, restaurant_id: int) -> List[Seats]:
    return list(session.scalars(
        select(Seats).where(Seats.restaurant_id == restaurant_id)
    ).all())


def delete_seats(session: Session, seats_id: int) -> bool:
    seats = session.get(Seats, seats_id)
    if not seats:
        return False
    session.delete(seats)
    session.commit()
    return True


# ============ BOOKING ============

def create_booking(session: Session, user_id: int, seats_id: int,
                   start_time: datetime, end_time: datetime,
                   guests_count: int, comment: Optional[str] = None,
                   status: str = "pending") -> Booking:
    booking = Booking(
        user_id=user_id,
        seats_id=seats_id,
        start_time=start_time,
        end_time=end_time,
        guests_count=guests_count,
        comment=comment,
        status=status,
    )
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking


def get_booking_by_id(session: Session, booking_id: int) -> Optional[Booking]:
    return session.get(Booking, booking_id)


def get_bookings_by_user(session: Session, user_id: int) -> List[Booking]:
    return list(session.scalars(
        select(Booking).where(Booking.user_id == user_id)
    ).all())


def get_bookings_by_status(session: Session, status: str) -> List[Booking]:
    return list(session.scalars(
        select(Booking).where(Booking.status == status)
    ).all())


def update_booking_status(session: Session, booking_id: int, status: str) -> Optional[Booking]:
    booking = session.get(Booking, booking_id)
    if not booking:
        return None
    booking.status = status
    session.commit()
    session.refresh(booking)
    return booking


def update_booking(session: Session, booking_id: int, **fields) -> Optional[Booking]:
    booking = session.get(Booking, booking_id)
    if not booking:
        return None
    for key, value in fields.items():
        if hasattr(booking, key):
            setattr(booking, key, value)
    session.commit()
    session.refresh(booking)
    return booking


def delete_booking(session: Session, booking_id: int) -> bool:
    booking = session.get(Booking, booking_id)
    if not booking:
        return False
    session.delete(booking)
    session.commit()
    return True


# ============ REVIEW ============

def create_review(session: Session, user_id: int, restaurant_id: int,
                  booking_id: int, rating: int,
                  text: Optional[str] = None) -> Review:
    review = Review(
        user_id=user_id,
        restaurant_id=restaurant_id,
        booking_id=booking_id,
        rating=rating,
        text=text,
    )
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


def get_review_by_id(session: Session, review_id: int) -> Optional[Review]:
    return session.get(Review, review_id)


def get_reviews_by_restaurant(session: Session, restaurant_id: int) -> List[Review]:
    return list(session.scalars(
        select(Review).where(Review.restaurant_id == restaurant_id)
    ).all())


def get_reviews_by_user(session: Session, user_id: int) -> List[Review]:
    return list(session.scalars(
        select(Review).where(Review.user_id == user_id)
    ).all())


def update_review(session: Session, review_id: int, **fields) -> Optional[Review]:
    review = session.get(Review, review_id)
    if not review:
        return None
    for key, value in fields.items():
        if hasattr(review, key):
            setattr(review, key, value)
    session.commit()
    session.refresh(review)
    return review


def delete_review(session: Session, review_id: int) -> bool:
    review = session.get(Review, review_id)
    if not review:
        return False
    session.delete(review)
    session.commit()
    return True


# ============ NOTIFICATION ============

def create_notification(session: Session, user_id: int, type_: str,
                        payload: Optional[dict] = None) -> Notification:
    notification = Notification(user_id=user_id, type=type_, payload=payload)
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


def get_notifications_by_user(session: Session, user_id: int) -> List[Notification]:
    return list(session.scalars(
        select(Notification).where(Notification.user_id == user_id)
    ).all())


def mark_notification_read(session: Session, notification_id: int) -> Optional[Notification]:
    notification = session.get(Notification, notification_id)
    if not notification:
        return None
    notification.is_read = True
    session.commit()
    session.refresh(notification)
    return notification


def delete_notification(session: Session, notification_id: int) -> bool:
    notification = session.get(Notification, notification_id)
    if not notification:
        return False
    session.delete(notification)
    session.commit()
    return True