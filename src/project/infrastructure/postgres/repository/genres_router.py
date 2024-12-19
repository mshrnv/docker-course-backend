from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.infrastructure.postgres.models import Genres
from project.schemas.models import GenreCreateUpdateSchema, GenreSchema
from project.core.exceptions import NotFound, AlreadyExists


class GenresRepository:
    _collection: Type[Genres] = Genres

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_genres(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        genres = await session.scalars(query)

        return [GenreSchema.model_validate(obj=genre) for genre in genres.all()]

    async def get_genre_by_id(
        self,
        session: AsyncSession,
        genre_id: int,
    ) -> GenreSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == genre_id)
        )

        genre = await session.scalar(query)

        if not genre:
            raise NotFound(message=f"Genre with id {genre_id} not found")

        return GenreSchema.model_validate(obj=genre)

    async def create_genre(
        self,
        session: AsyncSession,
        genre: GenreCreateUpdateSchema,
    ) -> GenreSchema:
        query = (
            insert(self._collection)
            .values(genre.model_dump())
            .returning(self._collection)
        )

        try:
            created_genre = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="Genre with the given details already exists")

        return GenreSchema.model_validate(obj=created_genre)

    async def update_genre(
        self,
        session: AsyncSession,
        genre_id: int,
        genre: GenreCreateUpdateSchema,
    ) -> GenreSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == genre_id)
            .values(genre.model_dump())
            .returning(self._collection)
        )

        updated_genre = await session.scalar(query)

        if not updated_genre:
            raise NotFound(message=f"Genre with id {genre_id} not found")

        return GenreSchema.model_validate(obj=updated_genre)

    async def delete_genre(
        self,
        session: AsyncSession,
        genre_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == genre_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"Genre with id {genre_id} not found")
