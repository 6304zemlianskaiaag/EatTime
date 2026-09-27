# models.py
from __future__ import annotations

from datetime import datetime, time
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import (
    BigInteger, String, Text, Boolean, Integer, SmallInteger,
    Numeric, Time, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    role: Mapped["Role"] = relationship(back_populates="users")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")
    restaurants: Mapped[List["Restaurant"]] = relationship(
        secondary="restaurant_admin", back_populates="admins"
    )


class Cuisine(Base):
    __tablename__ = "cuisine"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    restaurants: Mapped[List["Restaurant"]] = relationship(
        secondary="restaurant_cuisine", back_populates="cuisines"
    )


class RestaurantCuisine(Base):
    __tablename__ = "restaurant_cuisine"

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurant.id"), primary_key=True
    )
    cuisine_id: Mapped[int] = mapped_column(
        ForeignKey("cuisine.id"), primary_key=True
    )


class Restaurant(Base):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    opening_time: Mapped[time] = mapped_column(Time, nullable=False)
    closing_time: Mapped[time] = mapped_column(Time, nullable=False)
    avg_check: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    cuisines: Mapped[List["Cuisine"]] = relationship(
        secondary="restaurant_cuisine", back_populates="restaurants"
    )
    admins: Mapped[List["User"]] = relationship(
        secondary="restaurant_admin", back_populates="restaurants"
    )
    tables: Mapped[List["DiningTable"]] = relationship(back_populates="restaurant")
    seats: Mapped[List["Seats"]] = relationship(back_populates="restaurant")
    reviews: Mapped[List["Review"]] = relationship(back_populates="restaurant")


class RestaurantAdmin(Base):
    __tablename__ = "restaurant_admin"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurant.id"), primary_key=True
    )


class DiningTable(Base):
    __tablename__ = "dining_table"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(50))
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurant.id"), nullable=False
    )

    restaurant: Mapped["Restaurant"] = relationship(back_populates="tables")
    seats_links: Mapped[List["Seats"]] = relationship(back_populates="table")


class Seats(Base):
    __tablename__ = "Seats"

    seats_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    table_id: Mapped[int] = mapped_column(ForeignKey("dining_table.id"), primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurant.id"), primary_key=True
    )

    table: Mapped["DiningTable"] = relationship(back_populates="seats_links")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="seats")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="seats")


class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    guests_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="bookings")
    seats: Mapped["Seats"] = relationship(back_populates="bookings")
    review: Mapped[Optional["Review"]] = relationship(
        back_populates="booking", uselist=False
    )


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurant.id"), nullable=False
    )
    booking_id: Mapped[int] = mapped_column(
        ForeignKey("booking.id"), unique=True, nullable=False
    )
    rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    text: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="reviews")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="reviews")
    booking: Mapped["Booking"] = relationship(back_populates="review")


class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    payload: Mapped[Optional[dict]] = mapped_column(JSON)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="notifications")