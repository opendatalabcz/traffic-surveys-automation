from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from tsa import enums
from tsa.app.schemas.base import SourceFileModel
from tsa.app.schemas.source_file import SourceFileBase

from .base import DatabaseRepository


class SourceFileRepository(DatabaseRepository):
    model = SourceFileModel
    data_class = SourceFileBase
    sort_keys = [SourceFileModel.c.path]

    async def create(self, source_file: SourceFileBase, **_) -> Optional[SourceFileBase]:
        result_data = await self._connection.fetch_one(
            insert(self.model)
            .values(**source_file.dict(exclude_none=True))
            .on_conflict_do_nothing()
            .returning(self.model)
        )

        if result_data:
            return self.data_class(**result_data)

        return None

    async def update_state(self, source_file_id: int, new_state: enums.SourceFileStatus):
        await self.update(conditions=[self.model.c.id == source_file_id], status=new_state.value)
