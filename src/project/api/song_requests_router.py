from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import song_requests_repo
from project.schemas.models import SongRequestCreateUpdateSchema, SongRequestSchema
from project.core.exceptions import Error, ForeignKeyViolationError, NotFound

song_requests_router = APIRouter()

@song_requests_router.get(
    "/all_requests",
    response_model=list[SongRequestSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_requests() -> list[SongRequestSchema]:
    async with database.session() as session:
        all_requests = await song_requests_repo.get_all_song_requests(session)
    
    return all_requests


@song_requests_router.get(
    "/request/{id}",
    response_model=SongRequestSchema,
    status_code=status.HTTP_200_OK,
)
async def get_request_by_id(request_id: int) -> SongRequestSchema:
    try:
        async with database.session() as session:
            request = await song_requests_repo.get_song_request_by_id(session=session, song_request_id=request_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return request


@song_requests_router.post(
    "/add_request",
    response_model=SongRequestSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_request(request_dto: SongRequestCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_request = await song_requests_repo.create_song_request(session=session, song_request=request_dto)
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_request


@song_requests_router.put(
    "/update_request/{id}",
    response_model=SongRequestSchema,
    status_code=status.HTTP_200_OK,
)
async def update_request(request_id: int, request_dto: SongRequestCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_request = await song_requests_repo.update_song_request(
                session=session,
                request_id=request_id,
                song_request_id=request_dto,
            )
    except ForeignKeyViolationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_request


@song_requests_router.delete(
    "/delete_request/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_request(request_id: int):
    try:
        async with database.session() as session:
            request = await song_requests_repo.delete_song_request(session=session, song_request_id=request_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return request
