from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.infrastructure.postgres.models import PlaylistAndTrackPair, Playlists, Tracks
from project.schemas.models import PlaylistAndTrackPairCreateUpdateSchema, PlaylistAndTrackPairSchema
from project.core.exceptions import ForeignKeyViolationError, NotFound, AlreadyExists


class PlaylistAndTrackPairRepository:
    _collection: Type[PlaylistAndTrackPair] = PlaylistAndTrackPair

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

        return [PlaylistAndTrackPairSchema.model_validate(obj=pair) for pair in pairs.all()]

    async def get_pair_by_id(
        self,
        session: AsyncSession,
        pair_id: int,
    ) -> PlaylistAndTrackPairSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == pair_id)
        )

        pair = await session.scalar(query)

        if not pair:
            raise NotFound(message=f"Pair with id {pair_id} not found")

        return PlaylistAndTrackPairSchema.model_validate(obj=pair)

    async def create_pair(
        self,
        session: AsyncSession,
        pair: PlaylistAndTrackPairCreateUpdateSchema,
    ) -> PlaylistAndTrackPairSchema:
        query = (
            insert(self._collection)
            .values(pair.model_dump())
            .returning(self._collection)
        )

        playlist = await session.scalar(select(Playlists.id).where(self._collection.playlist_id == Playlists.id))
        if not playlist:
            raise ForeignKeyViolationError(message=f"Playlist with id {pair.playlist_id} not found")
        
        track = await session.scalar(select(Tracks.id).where(self._collection.track_id == Tracks.id))
        if not track:
            raise ForeignKeyViolationError(message=f"Track with id {pair.track_id} not found")

        try:
            created_pair = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="Pair with the given details already exists")

        return PlaylistAndTrackPairSchema.model_validate(obj=created_pair)

    async def update_pair(
        self,
        session: AsyncSession,
        pair_id: int,
        pair: PlaylistAndTrackPairCreateUpdateSchema,
    ) -> PlaylistAndTrackPairSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == pair_id)
            .values(pair.model_dump())
            .returning(self._collection)
        )

        playlist = await session.scalar(select(Playlists.id).where(self._collection.playlist_id == Playlists.id))
        if not playlist:
            raise ForeignKeyViolationError(message=f"Playlist with id {pair.playlist_id} not found")
        
        track = await session.scalar(select(Tracks.id).where(self._collection.track_id == Tracks.id))
        if not track:
            raise ForeignKeyViolationError(message=f"Track with id {pair.track_id} not found")

        updated_pair = await session.scalar(query)

        if not updated_pair:
            raise NotFound(message=f"Pair with id {pair_id} not found")

        return PlaylistAndTrackPairSchema.model_validate(obj=updated_pair)

    async def delete_pair(
        self,
        session: AsyncSession,
        pair_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == pair_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"Pair with id {pair_id} not found")
