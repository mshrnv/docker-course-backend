from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import playlist_track_repo
from project.schemas.models import PlaylistAndTrackPairCreateUpdateSchema, PlaylistAndTrackPairSchema
from project.core.exceptions import Error, ForeignKeyViolationError, NotFound

playlist_and_track_pair_router = APIRouter()

@playlist_and_track_pair_router.get(
    "/all_pairs",
    response_model=list[PlaylistAndTrackPairSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_pairs() -> list[PlaylistAndTrackPairSchema]:
    async with database.session() as session:
        all_pairs = await playlist_track_repo.get_all_pairs(session)
    
    return all_pairs


@playlist_and_track_pair_router.get(
    "/pair/{id}",
    response_model=PlaylistAndTrackPairSchema,
    status_code=status.HTTP_200_OK,
)
async def get_pair_by_id(pair_id: int) -> PlaylistAndTrackPairSchema:
    try:
        async with database.session() as session:
            pair = await playlist_track_repo.get_pair_by_id(session=session, pair_id=pair_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return pair


@playlist_and_track_pair_router.post(
    "/add_pair",
    response_model=PlaylistAndTrackPairSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_pair(pair_dto: PlaylistAndTrackPairCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_pair = await playlist_track_repo.create_pair(session=session, pair=pair_dto)
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_pair


@playlist_and_track_pair_router.put(
    "/update_pair/{id}",
    response_model=PlaylistAndTrackPairSchema,
    status_code=status.HTTP_200_OK,
)
async def update_pair(pair_id: int, pair_dto: PlaylistAndTrackPairCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_pair = await playlist_track_repo.update_pair(
                session=session,
                pair_id=pair_id,
                pair=pair_dto,
            )
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_pair


@playlist_and_track_pair_router.delete(
    "/delete_pair/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_pair(pair_id: int):
    try:
        async with database.session() as session:
            pair = await playlist_track_repo.delete_pair(session=session, pair_id=pair_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return pair
