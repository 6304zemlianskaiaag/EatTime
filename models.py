

# models.py
from datetime import datetime, time
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import (BigInteger, Boolean, CheckConstraint, DateTime, Enum, ForeignKey,
    Integer, Numeric, SmallInteger, String, Table, Column, Text, Time, func,)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship,)

import enum

class Base(DeclarativeBase):
    pass

class RestaurantStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    blocked = "blocked"

class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"

class NotificationType(str, enum.Enum):
    booking_created = "booking_created"
    booking_confirmed = "booking_confirmed"
    booking_rejected = "booking_rejected"
    booking_cancelled = "booking_cancelled"
    review_published = "review_published"

class TableLocation(str, enum.Enum):
    hall = "hall"
    terrace = "terrace"
    vip = "vip"
    bar = "bar"

class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, code={self.code!r})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    role: Mapped["Role"] = relationship(back_populates="users")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")
    restaurants: Mapped[List["Restaurant"]] = relationship(secondary="restaurant_admin",back_populates="admins",)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Restaurant(Base):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    opening_time: Mapped[time] = mapped_column(Time, nullable=False)
    closing_time: Mapped[time] = mapped_column(Time, nullable=False)
    avg_check: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[RestaurantStatus] = mapped_column(
        Enum(RestaurantStatus, name="restaurant_status"),
        nullable=False,
        default=RestaurantStatus.pending,
        server_default=RestaurantStatus.pending.value,)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    places: Mapped[List["Place"]] = relationship(back_populates="restaurant")
    admins: Mapped[List["User"]] = relationship(secondary="restaurant_admin",back_populates="restaurants",)
    cuisines: Mapped[List["Cuisine"]] = relationship(secondary="restaurant_cuisine",back_populates="restaurants",)

    def __repr__(self) -> str:
        return f"Restaurant(id={self.id!r}, name={self.name!r})"


class Cuisine(Base):
    __tablename__ = "cuisine"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    restaurants: Mapped[List["Restaurant"]] = relationship(secondary="restaurant_cuisine",back_populates="cuisines",)

    def __repr__(self) -> str:
        return f"Cuisine(id={self.id!r}, name={self.name!r})"


class TableType(Base):
    __tablename__ = "table_type"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[TableLocation] = mapped_column(Enum(TableLocation, name="table_location"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (CheckConstraint("seats > 0", name="ck_table_type_seats_positive"),)

    places: Mapped[List["Place"]] = relationship(back_populates="table_type")

    def __repr__(self) -> str:
        return f"TableType(id={self.id!r}, seats={self.seats!r})"


class Place(Base):
    __tablename__ = "place"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    type_table_id: Mapped[int] = mapped_column(ForeignKey("table_type.id"), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    table_type: Mapped["TableType"] = relationship(back_populates="places")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="places")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="place")

    def __repr__(self) -> str:
        return f"Place(id={self.id!r}, restaurant_id={self.restaurant_id!r})"


class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    place_id: Mapped[int] = mapped_column(ForeignKey("place.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    guests_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status"),
        nullable=False,
        default=BookingStatus.pending,
        server_default=BookingStatus.pending.value,)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("end_time > start_time", name="ck_booking_time_order"),
        CheckConstraint("guests_count > 0", name="ck_booking_guests_positive"),)

    user: Mapped["User"] = relationship(back_populates="bookings")
    place: Mapped["Place"] = relationship(back_populates="bookings")


    def __repr__(self) -> str:
        return f"Booking(id={self.id!r}, status={self.status!r})"


class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType, name="notification_type"), nullable=False)
    payload: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="notifications")

    def __repr__(self) -> str:
        return f"Notification(id={self.id!r}, type={self.type!r})"


#таблички для многое ко многим

restaurant_admin = Table("restaurant_admin", Base.metadata,
    Column("user_id", BigInteger, ForeignKey("user.id"), primary_key=True, ),
    Column("restaurant_id", BigInteger, ForeignKey("restaurant.id"), primary_key=True, ), )

restaurant_cuisine = Table("restaurant_cuisine",Base.metadata,
    Column("restaurant_id", BigInteger, ForeignKey("restaurant.id"), primary_key=True, ),
    Column("cuisine_id", Integer, ForeignKey("cuisine.id"), primary_key=True, ), )