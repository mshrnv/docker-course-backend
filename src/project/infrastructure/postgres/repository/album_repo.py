from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.infrastructure.postgres.models import Album
from project.schemas.models import AlbumCreateUpdateSchema, AlbumSchema
from project.core.exceptions import NotFound, AlreadyExists


class AlbumsRepository:
    _collection: Type[Album] = Album

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_all_albums(
        self,
        session: AsyncSession,
    ):
        query = select(self._collection)

        albums = await session.scalars(query)

        return [AlbumSchema.model_validate(obj=album) for album in albums.all()]

    async def get_album_by_id(
        self,
        session: AsyncSession,
        album_id: int,
    ) -> AlbumSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == album_id)
        )

        album = await session.scalar(query)

        if not album:
            raise NotFound(message=f"Album with id {album_id} not found")

        return AlbumSchema.model_validate(obj=album)

    async def create_album(
        self,
        session: AsyncSession,
        album: AlbumCreateUpdateSchema,
    ) -> AlbumSchema:
        query = (
            insert(self._collection)
            .values(album.model_dump())
            .returning(self._collection)
        )

        try:
            created_album = await session.scalar(query)
            await session.flush()
        except IntegrityError as error:
            raise AlreadyExists(message="Album with the given details already exists")

        return AlbumSchema.model_validate(obj=created_album)

    async def update_album(
        self,
        session: AsyncSession,
        album_id: int,
        album: AlbumCreateUpdateSchema,
    ) -> AlbumSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == album_id)
            .values(album.model_dump())
            .returning(self._collection)
        )

        updated_album = await session.scalar(query)

        if not updated_album:
            raise NotFound(message=f"Album with id {album_id} not found")

        return AlbumSchema.model_validate(obj=updated_album)

    async def delete_album(
        self,
        session: AsyncSession,
        album_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == album_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise NotFound(message=f"Album with id {album_id} not found")
