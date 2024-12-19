from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import albums_repo
from project.schemas.models import AlbumCreateUpdateSchema, AlbumSchema
from project.core.exceptions import Error, ForeignKeyViolationError, NotFound

albums_router = APIRouter()

@albums_router.get(
    "/all_albums",
    response_model=list[AlbumSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_albums() -> list[AlbumSchema]:
    async with database.session() as session:
        all_albums = await albums_repo.get_all_albums(session)
    
    return all_albums


@albums_router.get(
    "/album/{id}",
    response_model=AlbumSchema,
    status_code=status.HTTP_200_OK,
)
async def get_album_by_id(album_id: int) -> AlbumSchema:
    try:
        async with database.session() as session:
            album = await albums_repo.get_album_by_id(session=session, album_id=album_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return album


@albums_router.post(
    "/add_album",
    response_model=AlbumSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_album(album_dto: AlbumCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_album = await albums_repo.create_album(session=session, album=album_dto)
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_album


@albums_router.put(
    "/update_album/{id}",
    response_model=AlbumSchema,
    status_code=status.HTTP_200_OK,
)
async def update_album(album_id: int, album_dto: AlbumCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_album = await albums_repo.update_album(
                session=session,
                album_id=album_id,
                album=album_dto,
            )
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_album


@albums_router.delete(
    "/delete_album/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_album(album_id: int):
    try:
        async with database.session() as session:
            album = await albums_repo.delete_album(session=session, album_id=album_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return album
