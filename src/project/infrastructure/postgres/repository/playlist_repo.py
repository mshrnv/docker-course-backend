from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.infrastructure.postgres.models import Playlists, Programs
from project.schemas.models import PlaylistCreateUpdateSchema, PlaylistSchema
from project.core.exceptions import ForeignKeyViolationError, NotFound, AlreadyExists


class PlaylistsRepository:
    _collection: Type[Playlists] = Playlists

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_playlists(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        playlists = await session.scalars(query)

        return [PlaylistSchema.model_validate(obj=pl) for pl in playlists.all()]

    async def get_playlist_by_id(
        self,
        session: AsyncSession,
        playlist_id: int,
    ) -> PlaylistSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == playlist_id)
        )

        playlist = await session.scalar(query)

        if not playlist:
            raise NotFound(message=f"Playlist with id {playlist_id} not found")

        return PlaylistSchema.model_validate(obj=playlist)

    async def create_playlist(
        self,
        session: AsyncSession,
        playlist: PlaylistCreateUpdateSchema,
    ) -> PlaylistSchema:
        query = (
            insert(self._collection)
            .values(playlist.model_dump())
            .returning(self._collection)
        )

        program = await session.scalar(select(Programs.id).where(self._collection.program_id == Programs.id))
        if not program:
            raise ForeignKeyViolationError(message=f"Program with id {playlist.program_id} not found")

        try:
            created_playlist = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="Playlist with the given details already exists")

        return PlaylistSchema.model_validate(obj=created_playlist)

    async def update_playlist(
        self,
        session: AsyncSession,
        playlist_id: int,
        playlist: PlaylistCreateUpdateSchema,
    ) -> PlaylistSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == playlist_id)
            .values(playlist.model_dump())
            .returning(self._collection)
        )
        
        program = await session.scalar(select(Programs.id).where(self._collection.program_id == Programs.id))
        if not program:
            raise ForeignKeyViolationError(message=f"Program with id {playlist.program_id} not found")
        
        updated_playlist = await session.scalar(query)

        if not updated_playlist:
            raise NotFound(message=f"Playlist with id {playlist_id} not found")

        return PlaylistSchema.model_validate(obj=updated_playlist)

    async def delete_playlist(
        self,
        session: AsyncSession,
        playlist_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == playlist_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"Playlist with id {playlist_id} not found")
