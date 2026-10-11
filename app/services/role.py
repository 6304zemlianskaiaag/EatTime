# app/services/role.py
# Сервис Role — бизнес-логика

from typing import Optional, List

from app.models import Role
from app.repositories.role import RoleRepository
from app.schemas.role import RoleCreate


class RoleService:

    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def create(self, data: RoleCreate) -> Role:
        return self.repo.create(data)

    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self.repo.get_by_id(role_id)

    def get_by_code(self, code: str) -> Optional[Role]:
        return self.repo.get_by_code(code)

    def get_all(self) -> List[Role]:
        return self.repo.get_all()

    def update(self, role_id: int, new_name: str) -> Optional[Role]:
        return self.repo.update(role_id, new_name)

    def delete(self, role_id: int) -> bool:
        return self.repo.delete(role_id)