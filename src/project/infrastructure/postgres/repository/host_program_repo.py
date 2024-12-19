from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.infrastructure.postgres.models import HostProgramPair
from project.schemas.models import HostProgramPairCreateUpdateSchema, HostProgramPairSchema

from project.core.exceptions import NotFound, AlreadyExists, Error


class HostProgramPairRepository:
    _collection: Type[HostProgramPair] = HostProgramPair

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_pairs(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        pairs = await session.scalars(query)

        return [HostProgramPairSchema.model_validate(obj=pair) for pair in pairs.all()]

    async def get_pair_by_id(
        self,
        session: AsyncSession,
        pair_id: int,
    ) -> HostProgramPairSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == pair_id)
        )

        pair = await session.scalar(query)

        if not pair:
            raise NotFound(message=f"Pair with id {pair_id} not found")

        return HostProgramPairSchema.model_validate(obj=pair)

    async def create_pair(
        self,
        session: AsyncSession,
        pair: HostProgramPairCreateUpdateSchema,
    ) -> HostProgramPairSchema:
        query = (
            insert(self._collection)
            .values(pair.model_dump())
            .returning(self._collection)
        )

        try:
            created_pair = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="Pair with the given details already exists")

        return HostProgramPairSchema.model_validate(obj=created_pair)

    async def update_pair(
        self,
        session: AsyncSession,
        pair_id: int,
        pair: HostProgramPairCreateUpdateSchema,
    ) -> HostProgramPairSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == pair_id)
            .values(pair.model_dump())
            .returning(self._collection)
        )

        updated_pair = await session.scalar(query)

        if not updated_pair:
            raise NotFound(message=f"Pair with id {pair_id} not found")

        return HostProgramPairSchema.model_validate(obj=updated_pair)

    async def delete_pair(
        self,
        session: AsyncSession,
        pair_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == pair_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"Pair with id {pair_id} not found")
