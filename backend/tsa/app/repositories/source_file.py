from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from tsa import enums
from tsa.app.database import DatabaseRepository
from tsa.app.schemas.source_file import SourceFileBase, SourceFileModel


class SourceFileRepository(DatabaseRepository):
    async def create(self, source_file: SourceFileBase) -> Optional[SourceFileBase]:
        data = source_file.dict(exclude_none=True)
        statement = insert(SourceFileModel).values(**data).on_conflict_do_nothing().returning("*")

        raw_result = await self._connection.execute(statement)
        raw_result_value = raw_result.first()

        if raw_result_value:
            return SourceFileBase(**raw_result_value)

        return None

    async def list(self) -> List[SourceFileBase]:
        statement = select(SourceFileModel)

        raw_results = await self._connection.execute(statement)
        return [SourceFileBase(**raw_result) for raw_result in raw_results.all()]

    async def get(self, id_: int) -> SourceFileBase:
        statement = select(SourceFileModel).where(SourceFileModel.id == id_)

        raw_result = await self._connection.execute(statement)

        return SourceFileBase(**raw_result.one())

    async def update_state(self, source_file_id: int, new_state: enums.SourceFileStatus):
        statement = update(SourceFileModel).values(status=new_state.value).where(SourceFileModel.id == source_file_id)

        await self._connection.execute(statement)
