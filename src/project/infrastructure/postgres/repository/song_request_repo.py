from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.infrastructure.postgres.models import Programs, SongRequests, Tracks
from project.schemas.models import SongRequestCreateUpdateSchema, SongRequestSchema
from project.core.exceptions import ForeignKeyViolationError, NotFound, AlreadyExists


class SongRequestsRepository:
    _collection: Type[SongRequests] = SongRequests

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_song_requests(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        song_requests = await session.scalars(query)

        return [SongRequestSchema.model_validate(obj=sr) for sr in song_requests.all()]

    async def get_song_request_by_id(
        self,
        session: AsyncSession,
        song_request_id: int,
    ) -> SongRequestSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == song_request_id)
        )

        song_request = await session.scalar(query)

        if not song_request:
            raise NotFound(message=f"SongRequest with id {song_request_id} not found")

        return SongRequestSchema.model_validate(obj=song_request)

    async def create_song_request(
        self,
        session: AsyncSession,
        song_request: SongRequestCreateUpdateSchema,
    ) -> SongRequestSchema:
        query = (
            insert(self._collection)
            .values(song_request.model_dump())
            .returning(self._collection)
        )

        program = await session.scalar(select(Programs.id).where(self._collection.program_id == Programs.id))
        if not program:
            raise ForeignKeyViolationError(message=f"Program with id {song_request.program_id} not found")
        
        track = await session.scalar(select(Tracks.id).where(self._collection.track_id == Tracks.id))
        if not track:
            raise ForeignKeyViolationError(message=f"Track with id {song_request.track_id} not found")

        try:
            created_song_request = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="SongRequest with the given details already exists")

        return SongRequestSchema.model_validate(obj=created_song_request)

    async def update_song_request(
        self,
        session: AsyncSession,
        song_request_id: int,
        song_request: SongRequestCreateUpdateSchema,
    ) -> SongRequestSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == song_request_id)
            .values(song_request.model_dump())
            .returning(self._collection)
        )

        program = await session.scalar(select(Programs.id).where(self._collection.program_id == Programs.id))
        if not program:
            raise ForeignKeyViolationError(message=f"Program with id {song_request.program_id} not found")
        
        track = await session.scalar(select(Tracks.id).where(self._collection.track_id == Tracks.id))
        if not track:
            raise ForeignKeyViolationError(message=f"Track with id {song_request.track_id} not found")

        updated_song_request = await session.scalar(query)

        if not updated_song_request:
            raise NotFound(message=f"SongRequest with id {song_request_id} not found")

        return SongRequestSchema.model_validate(obj=updated_song_request)

    async def delete_song_request(
        self,
        session: AsyncSession,
        song_request_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == song_request_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"SongRequest with id {song_request_id} not found")
