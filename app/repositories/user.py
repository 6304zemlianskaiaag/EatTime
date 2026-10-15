from typing import Optional, List
from sqlalchemy.orm import Session

from app import crud
from app.models import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: UserCreate, password_hash: str) -> User:
        a = crud.create_user(
            self.session,
            email=data.email,
            password_hash=password_hash,
            full_name=data.full_name,
            role_id=data.role_id,
            phone=data.phone,
        )
        return a

    def get_by_id(self, user_id: int) -> Optional[User]:
        return crud.get_user_by_id(self.session, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return crud.get_user_by_email(self.session, email)

    def get_all(self) -> List[User]:
        return crud.get_all_users(self.session)

    def update(self, user_id: int, data: UserUpdate) -> Optional[User]:
        fields = data.model_dump(exclude_unset=True)
        return crud.update_user(self.session, user_id, **fields)

    def delete(self, user_id: int) -> bool:
        return crud.delete_user(self.session, user_id)