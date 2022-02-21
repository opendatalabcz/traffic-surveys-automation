from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from tsa import enums
from tsa.app.schemas.source_file import SourceFileBase, SourceFileModel

from .base import DatabaseRepository


class SourceFileRepository(DatabaseRepository[SourceFileModel, SourceFileBase]):
    model = SourceFileModel
    data_class = SourceFileBase

    async def create(self, source_file: SourceFileBase, **_) -> Optional[SourceFileBase]:
        result = await self._execute_statement(
            insert(self.model).values(**source_file.dict(exclude_none=True)).on_conflict_do_nothing().returning("*")
        )
        result_data = result.first()

        if result_data:
            return self.data_class(**result_data)

        return None

    async def update_state(self, source_file_id: int, new_state: enums.SourceFileStatus):
        await self.update(conditions=[self.model.id == source_file_id], status=new_state.value)
