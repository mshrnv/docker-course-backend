from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.infrastructure.postgres.models import Artists, Genres, Tracks
from project.schemas.models import TrackCreateUpdateSchema, TrackSchema
from project.core.exceptions import ForeignKeyViolationError, NotFound, AlreadyExists


class TracksRepository:
    _collection: Type[Tracks] = Tracks

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_tracks(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        tracks = await session.scalars(query)

        return [TrackSchema.model_validate(obj=track) for track in tracks.all()]

    async def get_track_by_id(
        self,
        session: AsyncSession,
        track_id: int,
    ) -> TrackSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == track_id)
        )

        track = await session.scalar(query)

        if not track:
            raise NotFound(message=f"Track with id {track_id} not found")

        return TrackSchema.model_validate(obj=track)

    async def create_track(
        self,
        session: AsyncSession,
        track: TrackCreateUpdateSchema,
    ) -> TrackSchema:
        query = (
            insert(self._collection)
            .values(track.model_dump())
            .returning(self._collection)
        )

        artist = await session.scalar(select(Artists.id).where(Tracks.artist_id == Artists.id))
        if not artist:
            raise ForeignKeyViolationError(message=f"Artist with id {track.artist_id} not found")

        genre = await session.scalar(select(Genres.id).where(Tracks.genre_id == Genres.id))
        if not genre:
            raise ForeignKeyViolationError(message=f"Genre with id {track.genre_id} not found")

        try:
            created_track = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="Track with the given details already exists")

        return TrackSchema.model_validate(obj=created_track)

    async def update_track(
        self,
        session: AsyncSession,
        track_id: int,
        track: TrackCreateUpdateSchema,
    ) -> TrackSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == track_id)
            .values(track.model_dump())
            .returning(self._collection)
        )

        artist = await session.scalar(select(Artists.id).where(Tracks.artist_id == Artists.id))
        if not artist:
            raise ForeignKeyViolationError(message=f"Artist with id {track.artist_id} not found")

        genre = await session.scalar(select(Genres.id).where(Tracks.genre_id == Genres.id))
        if not genre:
            raise ForeignKeyViolationError(message=f"Genre with id {track.genre_id} not found")

        updated_track = await session.scalar(query)

        if not updated_track:
            raise NotFound(message=f"Track with id {track_id} not found")

        return TrackSchema.model_validate(obj=updated_track)

    async def delete_track(
        self,
        session: AsyncSession,
        track_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == track_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"Track with id {track_id} not found")
