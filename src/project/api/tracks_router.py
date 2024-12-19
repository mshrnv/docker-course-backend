from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import tracks_repo
from project.schemas.models import TrackCreateUpdateSchema, TrackSchema
from project.core.exceptions import Error, NotFound

tracks_router = APIRouter()

@tracks_router.get(
    "/all_tracks",
    response_model=list[TrackSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_tracks() -> list[TrackSchema]:
    async with database.session() as session:
        all_tracks = await tracks_repo.get_all_tracks(session)
    
    return all_tracks


@tracks_router.get(
    "/track/{id}",
    response_model=TrackSchema,
    status_code=status.HTTP_200_OK,
)
async def get_track_by_id(track_id: int) -> TrackSchema:
    try:
        async with database.session() as session:
            track = await tracks_repo.get_track_by_id(session=session, track_id=track_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return track


@tracks_router.post(
    "/add_track",
    response_model=TrackSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_track(track_dto: TrackCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_track = await tracks_repo.create_track(session=session, track=track_dto)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_track


@tracks_router.put(
    "/update_track/{id}",
    response_model=TrackSchema,
    status_code=status.HTTP_200_OK,
)
async def update_track(track_id: int, track_dto: TrackCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_track = await tracks_repo.update_track(
                session=session,
                track_id=track_id,
                track=track_dto,
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_track


@tracks_router.delete(
    "/delete_track/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_track(track_id: int):
    try:
        async with database.session() as session:
            track = await tracks_repo.delete_track(session=session, track_id=track_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return track
