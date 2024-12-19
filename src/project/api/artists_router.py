from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import artists_repo
from project.schemas.models import ArtistCreateUpdateSchema, ArtistSchema
from project.core.exceptions import Error, NotFound, ForeignKeyViolationError

artists_router = APIRouter()

@artists_router.get(
    "/all_artists",
    response_model=list[ArtistSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_artists() -> list[ArtistSchema]:
    async with database.session() as session:
        all_artists = await artists_repo.get_all_artists(session)
    
    return all_artists


@artists_router.get(
    "/artist/{id}",
    response_model=ArtistSchema,
    status_code=status.HTTP_200_OK,
)
async def get_artist_by_id(artist_id: int) -> ArtistSchema:
    try:
        async with database.session() as session:
            artist = await artists_repo.get_artist_by_id(session=session, artist_id=artist_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return artist


@artists_router.post(
    "/add_artist",
    response_model=ArtistSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_artist(artist_dto: ArtistCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_artist = await artists_repo.create_artist(session=session, artist=artist_dto)
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_artist


@artists_router.put(
    "/update_artist/{id}",
    response_model=ArtistSchema,
    status_code=status.HTTP_200_OK,
)
async def update_artist(artist_id: int, artist_dto: ArtistCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_artist = await artists_repo.update_artist(
                session=session,
                artist_id=artist_id,
                artist=artist_dto,
            )
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_artist


@artists_router.delete(
    "/delete_artist/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_artist(artist_id: int):
    try:
        async with database.session() as session:
            artist = await artists_repo.delete_artist(session=session, artist_id=artist_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return artist
