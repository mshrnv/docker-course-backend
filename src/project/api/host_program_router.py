from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import host_program_repo
from project.schemas.models import HostProgramPairCreateUpdateSchema, HostProgramPairSchema
from project.core.exceptions import Error, NotFound

host_program_pair_router = APIRouter()

@host_program_pair_router.get(
    "/all_host_program_pairs",
    response_model=list[HostProgramPairSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_host_program_pairs() -> list[HostProgramPairSchema]:
    async with database.session() as session:
        all_host_program_pairs = await host_program_repo.get_all_host_program_pairs(session)
    
    return all_host_program_pairs


@host_program_pair_router.get(
    "/host_program_pair/{id}",
    response_model=HostProgramPairSchema,
    status_code=status.HTTP_200_OK,
)
async def get_host_program_pair_by_id(pair_id: int) -> HostProgramPairSchema:
    try:
        async with database.session() as session:
            pair = await host_program_repo.get_host_program_pair_by_id(session=session, pair_id=pair_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return pair


@host_program_pair_router.post(
    "/add_host_program_pair",
    response_model=HostProgramPairSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_host_program_pair(pair_dto: HostProgramPairCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_pair = await host_program_repo.create_host_program_pair(session=session, pair=pair_dto)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_pair


@host_program_pair_router.put(
    "/update_host_program_pair/{id}",
    response_model=HostProgramPairSchema,
    status_code=status.HTTP_200_OK,
)
async def update_host_program_pair(pair_id: int, pair_dto: HostProgramPairCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_pair = await host_program_repo.update_host_program_pair(
                session=session,
                pair_id=pair_id,
                pair=pair_dto,
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_pair


@host_program_pair_router.delete(
    "/delete_host_program_pair/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_host_program_pair(pair_id: int):
    try:
        async with database.session() as session:
            pair = await host_program_repo.delete_host_program_pair(session=session, pair_id=pair_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return pair
