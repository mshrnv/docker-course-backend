from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, PendingRollbackError, InterfaceError

from project.infrastructure.postgres.models import Programs
from project.schemas.models import ProgramCreateUpdateSchema, ProgramSchema

from project.core.exceptions import NotFound, AlreadyExists, Error


class ProgramsRepository:
    _collection: Type[Programs] = Programs

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_programs(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        programs = await session.scalars(query)

        return [ProgramSchema.model_validate(obj=prog) for prog in programs.all()]

    async def get_program_by_id(
        self,
        session: AsyncSession,
        program_id: int,
    ) -> ProgramSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == program_id)
        )

        program = await session.scalar(query)

        if not program:
            raise NotFound(_id=program_id)

        return ProgramSchema.model_validate(obj=program)

    async def create_program(
        self,
        session: AsyncSession,
        program: ProgramCreateUpdateSchema,
    ) -> ProgramSchema:
        query = (
            insert(self._collection)
            .values(program.model_dump())
            .returning(self._collection)
        )

        try:
            created_program = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise Error(message=repr(error))

        return ProgramSchema.model_validate(obj=created_program)

    async def update_program(
        self,
        session: AsyncSession,
        program_id: int,
        program: ProgramCreateUpdateSchema,
    ) -> ProgramSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == program_id)
            .values(program.model_dump())
            .returning(self._collection)
        )

        updated_program = await session.scalar(query)

        if not updated_program:
            raise NotFound(_id=program_id)

        return ProgramSchema.model_validate(obj=updated_program)

    async def delete_program(
        self,
        session: AsyncSession,
        program_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == program_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(_id=program_id)
        