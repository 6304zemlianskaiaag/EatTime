from __future__ import annotations
from db import SessionLocal, init_db
from crud import (
    create_role, get_all_roles,
    create_user, get_user_by_email,
    create_cuisine, create_restaurant,
    create_table, create_seats,
    create_booking, get_bookings_by_user,
    update_booking_status,
    create_review,
    create_notification, get_notifications_by_user,
    update_user, delete_user,
)

def main():
    init_db()  # на случай, если таблиц ещё нет
    session = SessionLocal()

    # 1. Роли
    if not get_all_roles(session):
        guest_role = create_role(session, "guest", "Гость")
        admin_role = create_role(session, "restaurant_admin", "Администратор ресторана")
        platform_role = create_role(session, "platform_admin", "Администратор платформы")
    else:
        guest_role = get_all_roles(session)[0]

    # 2. Пользователь
    user = create_user(
        session, "guest@mail.ru", "hash123",
        "Иван Иванов", role_id=guest_role.id, phone="+79990001122"
    )
    print("Создан пользователь:", user.id, user.email)

    # 3. Кухня и ресторан
    cuisine = create_cuisine(session, "Итальянская")
    from datetime import time
    restaurant = create_restaurant(
        session,
        name="Trattoria",
        address="ул. Ленина, 1",
        opening_time=time(10, 0),
        closing_time=time(23, 0),
        description="Итальянский ресторан",
        cuisine_ids=[cuisine.id],
        status="approved",
    )
    print("Создан ресторан:", restaurant.id, restaurant.name)

    # 4. Столик и место
    table = create_table(session, seats=4, restaurant_id=restaurant.id, location="hall")
    seats = create_seats(session, seats_id=1, table_id=table.id,
                         restaurant_id=restaurant.id)
    print("Создан столик:", table.id, "место:", seats.seats_id)

    # 5. Бронь
    from datetime import datetime, timedelta
    booking = create_booking(
        session,
        user_id=user.id,
        seats_id=seats.seats_id,
        start_time=datetime.now() + timedelta(days=1),
        end_time=datetime.now() + timedelta(days=1, hours=2),
        guests_count=2,
        comment="У окна",
    )
    print("Создана бронь:", booking.id, booking.status)

    # 6. Подтверждение
    booking = update_booking_status(session, booking.id, "confirmed")
    print("Статус брони:", booking.status)

    # 7. Отзыв
    booking = update_booking_status(session, booking.id, "completed")
    review = create_review(
        session, user_id=user.id,
        restaurant_id=restaurant.id,
        booking_id=booking.id,
        rating=5,
        text="Всё понравилось",
    )
    print("Создан отзыв:", review.id, review.rating)

    # 8. Уведомление
    notif = create_notification(
        session, user.id, "booking_confirmed",
        payload={"booking_id": booking.id}
    )
    print("Создано уведомление:", notif.id, notif.type)

    # 9. Обновление пользователя
    user = update_user(session, user.id, phone="+79995556677")
    print("Телефон обновлён:", user.phone)

    # 10. Чтение
    print("Брони пользователя:", [b.id for b in get_bookings_by_user(session, user.id)])
    print("Уведомления:", [n.id for n in get_notifications_by_user(session, user.id)])

    # 11. Удаление
    # delete_user(session, user.id)  # раскомментируйте, если хотите проверить удаление
    # print("Пользователь удалён")

    session.close()


if __name__ == "__main__":
    main()