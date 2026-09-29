from datetime import datetime, time, timedelta
from decimal import Decimal
from sqlalchemy import select, func

from db import SessionLocal
from models import (Role, User, Restaurant, Cuisine, TableType, Place, Booking, Notification,
    RestaurantStatus, BookingStatus, NotificationType, TableLocation, )
import crud as c1

def main():
    session = SessionLocal()
    try:
       print("\nКухни:")
        for cu in c1.get_all_cuisines(session):
            print(f"  - {cu.id}: {cu.name}")

       print("\n2. Поиск ресторанов по кухне 'Итальянская'")
        italian_restaurants = c1.search_restaurants_by_cuisine(session, "Итальянская")
        for r in italian_restaurants:
            cuisines = [c.name for c in r.cuisines]
            print(f"  - {r.name} ({r.address}), кухни: {cuisines}")

        print("\n3. Карточка ресторана La sushi")
        sushi = session.scalar(select(Restaurant).where(Restaurant.name == "Sushi Master"))
        sushi = c1.get_restaurant_by_id(session, sushi.id)
        print(f"  Название:    {sushi.name}")
        print(f"  Адрес:       {sushi.address}")
        print(f"  Телефон:     {sushi.phone}")
        print(f"  Часы работы: {sushi.opening_time} – {sushi.closing_time}")
        print(f"  Средний чек: {sushi.avg_check}")
        print(f"  Статус:      {sushi.status.value}")
        print(f"  Кухни:       {[c.name for c in sushi.cuisines]}")
        print(f"  Админы:      {[u.full_name for u in sushi.admins]}")
        print(f"  Столики:")
        for p in sushi.places:
            print(f"    - Place #{p.id}: {p.table_type.seats} мест, "
                  f"{p.table_type.location.value}, active={p.is_active}")

        print("\n4. Бронирование столика (Create)")
        ivan = session.scalar(select(User).where(User.email == "ivan@example.com"))
        free_place = session.scalar(
            select(Place)
            .where(Place.restaurant_id == sushi.id, Place.is_active.is_(True))
            .order_by(Place.id)
        )
        start = datetime.now().replace(microsecond=0) + timedelta(days=7, hours=3)
        end = start + timedelta(hours=2)
        new_booking = c1.create_booking(session, ivan.id, free_place.id, start, end, guests_count=2, comment="Демонстрационная бронь",)
        print(f"  Создана бронь #{new_booking.id}")
        print(f"  Столик:   Place #{free_place.id} ({free_place.table_type.seats} мест)")
        print(f"  Время:    {new_booking.start_time} – {new_booking.end_time}")
        print(f"  Статус:   {new_booking.status.value}")

        print("\n5. Попытка забронировать тот же столик на пересекающееся время")
        try:
            c1.create_booking(
                session, ivan.id, free_place.id,
                start + timedelta(minutes=30),
                end + timedelta(minutes=30),
                guests_count=2,
            )
        except ValueError as e:
            print(f"  Ожидаемая ошибка: {e}")


        print("\n6. Подтверждение брони администратором ресторана")
        print(f"  До:    status={new_booking.status.value}")
        c1.update_booking_status(session, new_booking.id, BookingStatus.confirmed)
        updated = c1.get_booking(session, new_booking.id)
        print(f"  После: status={updated.status.value}")

        print("\n7. Входящие брони ресторана La sushi (только confirmed)")
        bookings = c1.get_bookings_by_restaurant(
            session, sushi.id, status=BookingStatus.confirmed
        )
        for b in bookings:
            print(f"  Бронь #{b.id}: {b.user.full_name}, "
                  f"{b.start_time} – {b.end_time}, "
                  f"{b.guests_count} гостей, статус={b.status.value}")

        print("\n8. Отмена брони гостем")
        maria = session.scalar(select(User).where(User.email == "maria@example.com"))
        maria_booking = session.scalar(
            select(Booking)
            .where(Booking.user_id == maria.id,
                   Booking.status == BookingStatus.confirmed)
        )
        if maria_booking:
            print(f"  Бронь #{maria_booking.id} до отмены: {maria_booking.status.value}")
            ok = c1.cancel_booking(session, maria_booking.id, maria.id)
            session.refresh(maria_booking)
            print(f"  Отмена выполнена: {ok}")
            print(f"  После: {maria_booking.status.value}")


        print("\n 9. Уведомления гостя Ивана")
        notif = c1.create_notification(
            session, ivan.id, NotificationType.booking_confirmed,
            {"booking_id": new_booking.id},
        )
        print(f"  Создано уведомление #{notif.id}, is_read={notif.is_read}")

        unread = c1.get_notifications_by_user(session, ivan.id, only_unread=True)
        print(f"  Непрочитанных у Ивана: {len(unread)}")
        c1.mark_notification_read(session, notif.id)
        unread_after = c1.get_notifications_by_user(session, ivan.id, only_unread=True)
        print(f"  После отметки 'прочитано': {len(unread_after)}")


        print("\n 10. Удаление демонстрационной брони")
        print(f"  Бронь #{new_booking.id} до удаления: "
              f"{c1.get_booking(session, new_booking.id) is not None}")
        c1.delete_booking(session, new_booking.id)
        print(f"  Бронь #{new_booking.id} после удаления: "
              f"{c1.get_booking(session, new_booking.id) is not None}")


    finally:
        session.close()


if __name__ == "__main__":
    main()