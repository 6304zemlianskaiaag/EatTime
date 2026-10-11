# app/services/table_type.py
# Сервис TableType — бизнес-логика

from typing import Optional, List

from app.models import TableType
from app.repositories.table_type import TableTypeRepository
from app.schemas.table_type import TableTypeCreate


class TableTypeService:

    def __init__(self, repo: TableTypeRepository):
        self.repo = repo

    def create(self, data: TableTypeCreate) -> TableType:
        return self.repo.create(data)

    def get_by_id(self, tt_id: int) -> Optional[TableType]:
        return self.repo.get_by_id(tt_id)

    def get_all(self) -> List[TableType]:
        return self.repo.get_all()

    def update(self, tt_id: int, **fields) -> Optional[TableType]:
        return self.repo.update(tt_id, **fields)

    def delete(self, tt_id: int) -> bool:
        return self.repo.delete(tt_id)