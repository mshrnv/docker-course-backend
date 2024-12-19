from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, PendingRollbackError, InterfaceError

from project.infrastructure.postgres.models import Hosts
from project.schemas.models import HostCreateUpdateSchema, HostSchema

from project.core.exceptions import NotFound, AlreadyExists, Error


class HostsRepository:
    _collection: Type[Hosts] = Hosts

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_hosts(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        hosts = await session.scalars(query)

        return [HostSchema.model_validate(obj=host) for host in hosts.all()]

    async def get_host_by_id(
        self,
        session: AsyncSession,
        host_id: int,
    ) -> HostSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == host_id)
        )

        host = await session.scalar(query)

        if not host:
            raise NotFound(message=f"Host with id {host_id} not found")

        return HostSchema.model_validate(obj=host)

    async def create_host(
        self,
        session: AsyncSession,
        host: HostCreateUpdateSchema,
    ) -> HostSchema:
        query = (
            insert(self._collection)
            .values(host.model_dump())
            .returning(self._collection)
        )

        try:
            created_host = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="Host with the given details already exists")

        return HostSchema.model_validate(obj=created_host)

    async def update_host(
        self,
        session: AsyncSession,
        host_id: int,
        host: HostCreateUpdateSchema,
    ) -> HostSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == host_id)
            .values(host.model_dump())
            .returning(self._collection)
        )

        updated_host = await session.scalar(query)

        if not updated_host:
            raise NotFound(message=f"Host with id {host_id} not found")

        return HostSchema.model_validate(obj=updated_host)

    async def delete_host(
        self,
        session: AsyncSession,
        host_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == host_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"Host with id {host_id} not found")
