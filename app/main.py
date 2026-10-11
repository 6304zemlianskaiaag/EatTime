# app/main.py
# Точка входа FastAPI-приложения

from fastapi import FastAPI

from app.api import auth, users, restaurants, bookings, cuisines, notifications, places, table_types, roles

app = FastAPI(
    title="EatTime API",
    description="API для онлайн-бронирования столиков",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(bookings.router)
app.include_router(cuisines.router)
app.include_router(notifications.router)
app.include_router(places.router)
app.include_router(table_types.router)
app.include_router(roles.router)


@app.get("/")
def root():
    return {"message": "EatTime API работает"}