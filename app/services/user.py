# app/services/user.py
# Сервис User — бизнес-логика

from typing import Optional, List

from app.models import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.security import hash_password


# Сервис для работы с пользователями
class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    # Регистрирует пользователя: проверяет email, хеширует пароль
    def register(self, data: UserCreate) -> User:
        if self.repo.get_by_email(data.email):
            raise ValueError("Email уже занят")
        password_hash = hash_password(data.password)
        return self.repo.create(data, password_hash)

    # Возвращает пользователя по ID
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    # Возвращает пользователя по email
    def get_by_email(self, email: str) -> Optional[User]:
        return self.repo.get_by_email(email)

    # Возвращает список всех пользователей
    def get_all(self) -> List[User]:
        return self.repo.get_all()

    # Обновляет пользователя
    def update(self, user_id: int, data: UserUpdate) -> Optional[User]:
        return self.repo.update(user_id, data)

    # Удаляет пользователя
    def delete(self, user_id: int) -> bool:
        return self.repo.delete(user_id)