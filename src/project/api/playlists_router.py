from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import playlists_repo
from project.schemas.models import PlaylistCreateUpdateSchema, PlaylistSchema
from project.core.exceptions import Error, ForeignKeyViolationError, NotFound

playlists_router = APIRouter()

@playlists_router.get(
    "/all_playlists",
    response_model=list[PlaylistSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_playlists() -> list[PlaylistSchema]:
    async with database.session() as session:
        all_playlists = await playlists_repo.get_all_playlists(session)
    
    return all_playlists


@playlists_router.get(
    "/playlist/{id}",
    response_model=PlaylistSchema,
    status_code=status.HTTP_200_OK,
)
async def get_playlist_by_id(playlist_id: int) -> PlaylistSchema:
    try:
        async with database.session() as session:
            playlist = await playlists_repo.get_playlist_by_id(session=session, playlist_id=playlist_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return playlist


@playlists_router.post(
    "/add_playlist",
    response_model=PlaylistSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_playlist(playlist_dto: PlaylistCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_playlist = await playlists_repo.create_playlist(session=session, playlist=playlist_dto)
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_playlist


@playlists_router.put(
    "/update_playlist/{id}",
    response_model=PlaylistSchema,
    status_code=status.HTTP_200_OK,
)
async def update_playlist(playlist_id: int, playlist_dto: PlaylistCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_playlist = await playlists_repo.update_playlist(
                session=session,
                playlist_id=playlist_id,
                playlist=playlist_dto,
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_playlist


@playlists_router.delete(
    "/delete_playlist/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_playlist(playlist_id: int):
    try:
        async with database.session() as session:
            playlist = await playlists_repo.delete_playlist(session=session, playlist_id=playlist_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return playlist
