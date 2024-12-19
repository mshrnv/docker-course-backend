from fastapi import APIRouter, HTTPException, status
from project.api.depends import database
from project.api.depends import hosts_repo
from project.schemas.models import HostCreateUpdateSchema, HostSchema
from project.core.exceptions import Error, NotFound

host_router = APIRouter()

@host_router.get(
    "/all_hosts",
    response_model=list[HostSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_hosts() -> list[HostSchema]:
    async with database.session() as session:
        all_hosts = await hosts_repo.get_all_hosts(session)
    
    return all_hosts


@host_router.get(
    "/host/{id}",
    response_model=HostSchema,
    status_code=status.HTTP_200_OK,
)
async def get_host_by_id(host_id: int) -> HostSchema:
    try:
        async with database.session() as session:
            host = await hosts_repo.get_host_by_id(session=session, host_id=host_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return host


@host_router.post(
    "/add_host",
    response_model=HostSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_host(host_dto: HostCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_host = await hosts_repo.create_host(session=session, host=host_dto)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_host


@host_router.put(
    "/update_host/{id}",
    response_model=HostSchema,
    status_code=status.HTTP_200_OK,
)
async def update_host(host_id: int, host_dto: HostCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_host = await hosts_repo.update_host(
                session=session,
                host_id=host_id,
                host=host_dto,
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_host


@host_router.delete(
    "/delete_host/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_host(host_id: int):
    try:
        async with database.session() as session:
            host = await hosts_repo.delete_host(session=session, host_id=host_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return host
