# app/repositories/table_type.py
# Репозиторий TableType — обёртка над crud.py

from typing import Optional, List
from sqlalchemy.orm import Session

from app import crud
from app.models import TableType, TableLocation
from app.schemas.table_type import TableTypeCreate


class TableTypeRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: TableTypeCreate) -> TableType:
        return crud.create_table_type(
            self.session,
            seats=data.seats,
            location=TableLocation(data.location),
        )

    def get_by_id(self, tt_id: int) -> Optional[TableType]:
        return crud.get_table_type(self.session, tt_id)

    def get_all(self) -> List[TableType]:
        return crud.get_all_table_types(self.session)

    def update(self, tt_id: int, **fields) -> Optional[TableType]:
        return crud.update_table_type(self.session, tt_id, **fields)

    def delete(self, tt_id: int) -> bool:
        return crud.delete_table_type(self.session, tt_id)