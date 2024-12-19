from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import genres_repo
from project.schemas.models import GenreCreateUpdateSchema, GenreSchema
from project.core.exceptions import Error, NotFound

genres_router = APIRouter()

@genres_router.get(
    "/all_genres",
    response_model=list[GenreSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_genres() -> list[GenreSchema]:
    async with database.session() as session:
        all_genres = await genres_repo.get_all_genres(session)
    
    return all_genres


@genres_router.get(
    "/genre/{id}",
    response_model=GenreSchema,
    status_code=status.HTTP_200_OK,
)
async def get_genre_by_id(genre_id: int) -> GenreSchema:
    try:
        async with database.session() as session:
            genre = await genres_repo.get_genre_by_id(session=session, genre_id=genre_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return genre


@genres_router.post(
    "/add_genre",
    response_model=GenreSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_genre(genre_dto: GenreCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_genre = await genres_repo.create_genre(session=session, genre=genre_dto)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_genre


@genres_router.put(
    "/update_genre/{id}",
    response_model=GenreSchema,
    status_code=status.HTTP_200_OK,
)
async def update_genre(genre_id: int, genre_dto: GenreCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_genre = await genres_repo.update_genre(
                session=session,
                genre_id=genre_id,
                genre=genre_dto,
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_genre


@genres_router.delete(
    "/delete_genre/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_genre(genre_id: int):
    try:
        async with database.session() as session:
            genre = await genres_repo.delete_genre(session=session, genre_id=genre_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return genre
