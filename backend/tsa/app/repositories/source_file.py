from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from tsa.app.database import DatabaseRepository
from tsa.app.schemas import SourceFileModel


class SourceFileRepository(DatabaseRepository):
    async def create(self, source_file: SourceFileModel) -> Optional[SourceFileModel]:
        data = source_file.dict(exclude_none=True)
        statement = insert(SourceFileModel).values(**data).on_conflict_do_nothing().returning("*")

        raw_result = await self._connection.execute(statement)
        raw_result_value = raw_result.first()

        if raw_result_value:
            return SourceFileModel(**raw_result_value)

        return None

    async def list(self) -> List[SourceFileModel]:
        statement = select(SourceFileModel)

        raw_results = await self._connection.execute(statement)
        return [SourceFileModel(**raw_result) for raw_result in raw_results.all()]

    async def get(self, id_: int) -> SourceFileModel:
        statement = select(SourceFileModel).where(SourceFileModel.id == id_)

        raw_result = await self._connection.execute(statement)

        return SourceFileModel(**raw_result.one())
