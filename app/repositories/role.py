# app/repositories/role.py
# Репозиторий Role — обёртка над crud.py

from typing import Optional, List
from sqlalchemy.orm import Session

from app import crud
from app.models import Role
from app.schemas.role import RoleCreate


class RoleRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: RoleCreate) -> Role:
        return crud.create_role(self.session, code=data.code, name=data.name)

    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self.session.get(Role, role_id)

    def get_by_code(self, code: str) -> Optional[Role]:
        return crud.get_role_by_code(self.session, code)

    def get_all(self) -> List[Role]:
        return crud.get_all_roles(self.session)

    def update(self, role_id: int, new_name: str) -> Optional[Role]:
        return crud.update_role(self.session, role_id, new_name)

    def delete(self, role_id: int) -> bool:
        return crud.delete_role(self.session, role_id)