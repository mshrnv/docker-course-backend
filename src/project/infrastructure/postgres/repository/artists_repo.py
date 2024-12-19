from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.infrastructure.postgres.models import Artists, Genres
from project.schemas.models import ArtistCreateUpdateSchema, ArtistSchema
from project.core.exceptions import ForeignKeyViolationError, NotFound, AlreadyExists


class ArtistsRepository:
    _collection: Type[Artists] = Artists

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_artists(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        artists = await session.scalars(query)

        return [ArtistSchema.model_validate(obj=artist) for artist in artists.all()]

    async def get_artist_by_id(
        self,
        session: AsyncSession,
        artist_id: int,
    ) -> ArtistSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == artist_id)
        )

        artist = await session.scalar(query)

        if not artist:
            raise NotFound(message=f"Artist with id {artist_id} not found")

        return ArtistSchema.model_validate(obj=artist)

    async def create_artist(
        self,
        session: AsyncSession,
        artist: ArtistCreateUpdateSchema,
    ) -> ArtistSchema:
        query = (
            insert(self._collection)
            .values(artist.model_dump())
            .returning(self._collection)
        )

        genre = await session.scalar(select(Genres.id).where(Artists.genre_id == Genres.id))
        if not genre:
            raise ForeignKeyViolationError(message=f"Genre with id {artist.genre_id} not found")

        try:
            created_artist = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="Artist with the given details already exists")

        return ArtistSchema.model_validate(obj=created_artist)

    async def update_artist(
        self,
        session: AsyncSession,
        artist_id: int,
        artist: ArtistCreateUpdateSchema,
    ) -> ArtistSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == artist_id)
            .values(artist.model_dump())
            .returning(self._collection)
        )

        genre = await session.scalar(select(Genres.id).where(Artists.genre_id == Genres.id))
        if not genre:
            raise ForeignKeyViolationError(message=f"Genre with id {artist.genre_id} not found")

        updated_artist = await session.scalar(query)

        if not updated_artist:
            raise NotFound(message=f"Artist with id {artist_id} not found")

        return ArtistSchema.model_validate(obj=updated_artist)

    async def delete_artist(
        self,
        session: AsyncSession,
        artist_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == artist_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"Artist with id {artist_id} not found")
