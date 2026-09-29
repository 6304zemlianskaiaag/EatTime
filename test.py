from datetime import datetime, time, timedelta
from decimal import Decimal

from db import engine, SessionLocal
from models import (Base, Role, User, Restaurant, Cuisine, TableType, Place, Booking, Notification,
    RestaurantStatus, BookingStatus, NotificationType, TableLocation, restaurant_admin, restaurant_cuisine,)

def seed():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        roles = [
            Role(code="guest", name="Гость"),
            Role(code="restaurant_admin", name="Администратор ресторана"),
            Role(code="platform_admin", name="Администратор платформы"),
        ]
        session.add_all(roles)
        session.commit()

        guest_role, rest_admin_role, platform_admin_role = roles

        users = [
            User(
                email="ivan@example.com",
                password_hash="hash_ivan",
                full_name="Иван Иванов",
                phone="+79990000001",
                role_id=guest_role.id,
            ),
            User(
                email="maria@example.com",
                password_hash="hash_maria",
                full_name="Мария Петрова",
                phone="+79990000002",
                role_id=guest_role.id,
            ),
            User(
                email="admin@lapiazza.ru",
                password_hash="hash_admin1",
                full_name="Пётр Сидоров",
                phone="+79990000003",
                role_id=rest_admin_role.id,
            ),
            User(
                email="admin@sushi.ru",
                password_hash="hash_admin2",
                full_name="Анна Кузнецова",
                phone="+79990000004",
                role_id=rest_admin_role.id,
            ),
            User(
                email="platform@booking.ru",
                password_hash="hash_platform",
                full_name="Сергей Модератов",
                phone="+79990000005",
                role_id=platform_admin_role.id,
            ),
        ]
        session.add_all(users)
        session.commit()

        ivan, maria, admin_piazza, admin_sushi, platform_admin = users

        cuisines = [
            Cuisine(name="Итальянская"),
            Cuisine(name="Японская"),
            Cuisine(name="Русская"),
            Cuisine(name="Французская"),
        ]
        session.add_all(cuisines)
        session.commit()

        italian, japanese, russian, french = cuisines

        restaurants = [
            Restaurant(
                name="La Piazza",
                description="Итальянский ресторан в центре города",
                address="г. Самара, ул. Ленина, 1",
                phone="+78462000001",
                opening_time=time(10, 0),
                closing_time=time(23, 0),
                avg_check=Decimal("2500.00"),
                status=RestaurantStatus.approved,
            ),
            Restaurant(
                name="Sushi Master",
                description="Японская кухня, суши и роллы",
                address="г. Самара, ул. Мира, 15",
                phone="+78462000002",
                opening_time=time(11, 0),
                closing_time=time(22, 0),
                avg_check=Decimal("1800.00"),
                status=RestaurantStatus.approved,
            ),
            Restaurant(
                name="Тройка",
                description="Русская кухня, домашняя атмосфера",
                address="г. Самара, ул. Победы, 7",
                phone="+78462000003",
                opening_time=time(9, 0),
                closing_time=time(21, 0),
                avg_check=Decimal("1200.00"),
                status=RestaurantStatus.pending,
            ),
        ]
        session.add_all(restaurants)
        session.commit()

        piazza, sushi, troika = restaurants

        piazza.cuisines.extend([italian, french])
        sushi.cuisines.extend([japanese])
        troika.cuisines.extend([russian, italian])
        session.commit()

        admin_piazza.restaurants.append(piazza)
        admin_sushi.restaurants.append(sushi)
        admin_sushi.restaurants.append(troika)   # один админ — два ресторана
        session.commit()

        table_types = [
            TableType(seats=2, location=TableLocation.hall),
            TableType(seats=4, location=TableLocation.hall),
            TableType(seats=6, location=TableLocation.vip),
            TableType(seats=2, location=TableLocation.terrace),
        ]
        session.add_all(table_types)
        session.commit()

        tt2_hall, tt4_hall, tt6_vip, tt2_terrace = table_types

        places = [
            Place(type_table_id=tt2_hall.id, restaurant_id=piazza.id, is_active=True),
            Place(type_table_id=tt4_hall.id, restaurant_id=piazza.id, is_active=True),
            Place(type_table_id=tt2_hall.id, restaurant_id=sushi.id, is_active=True),
            Place(type_table_id=tt2_terrace.id, restaurant_id=sushi.id, is_active=True),
            Place(type_table_id=tt4_hall.id, restaurant_id=troika.id, is_active=True),
            Place(type_table_id=tt6_vip.id, restaurant_id=troika.id, is_active=False),  # неактивный
        ]
        session.add_all(places)
        session.commit()

        piazza_place2, piazza_place4, sushi_place2, sushi_terrace, troika_place4, troika_vip = places

        now = datetime.now().replace(microsecond=0)

        bookings = [
            Booking(
                user_id=ivan.id,
                place_id=piazza_place4.id,
                start_time=now + timedelta(days=1, hours=3),
                end_time=now + timedelta(days=1, hours=5),
                guests_count=3,
                status=BookingStatus.pending,
                comment="Столик у окна",
            ),
            Booking(
                user_id=maria.id,
                place_id=sushi_place2.id,
                start_time=now + timedelta(days=2, hours=2),
                end_time=now + timedelta(days=2, hours=4),
                guests_count=2,
                status=BookingStatus.confirmed,
                comment=None,
            ),
            Booking(
                user_id=ivan.id,
                place_id=sushi_terrace.id,
                start_time=now - timedelta(days=3, hours=2),
                end_time=now - timedelta(days=3),
                guests_count=2,
                status=BookingStatus.completed,
                comment="Годовщина",
            ),
            Booking(
                user_id=maria.id,
                place_id=piazza_place2.id,
                start_time=now + timedelta(days=4, hours=1),
                end_time=now + timedelta(days=4, hours=3),
                guests_count=2,
                status=BookingStatus.cancelled,
                comment=None,
            ),
            Booking(
                user_id=ivan.id,
                place_id=troika_place4.id,
                start_time=now + timedelta(days=5, hours=2),
                end_time=now + timedelta(days=5, hours=4),
                guests_count=4,
                status=BookingStatus.rejected,
                comment="Прошу тихий столик",
            ),
        ]
        session.add_all(bookings)
        session.commit()

        booking_pending, booking_confirmed, booking_completed, booking_cancelled, booking_rejected = bookings

notifications = [
            Notification(
                user_id=ivan.id,
                type=NotificationType.booking_created,
                payload={"booking_id": booking_pending.id},
                is_read=False,
            ),
            Notification(
                user_id=maria.id,
                type=NotificationType.booking_confirmed,
                payload={"booking_id": booking_confirmed.id},
                is_read=True,
            ),
            Notification(
                user_id=maria.id,
                type=NotificationType.booking_cancelled,
                payload={"booking_id": booking_cancelled.id},
                is_read=True,
            ),
        ]
        session.add_all(notifications)
        session.commit()

if __name__ == "__main__":
    seed()