from fastapi import APIRouter, HTTPException, status, Depends

from project.api.depends import database
from project.api.depends import programs_repo
from project.schemas.models import ProgramCreateUpdateSchema, ProgramSchema
from project.core.exceptions import Error, NotFound, AlreadyExists


program_router = APIRouter()

@program_router.get(
    "/all_programs",
    response_model=list[ProgramSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_programs() -> list[ProgramSchema]:
    async with database.session() as session:
        all_programs = await programs_repo.get_all_programs(session)
    
    return all_programs


@program_router.get(
    "/program/{id}",
    response_model=ProgramSchema,
    status_code=status.HTTP_200_OK,
)
async def get_program_by_id(program_id: int) -> ProgramSchema:
    try:
        async with database.session() as session:
            program = await programs_repo.get_program_by_id(session=session, program_id=program_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return program



@program_router.post(
    "/add_program",
    response_model=ProgramSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_program(program_dto: ProgramCreateUpdateSchema):
    try:
        async with database.session() as session:
            new_program = await programs_repo.create_program(session=session, program=program_dto)
    except Error as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_program


@program_router.put(
    "/update_program/{id}",
    response_model=ProgramSchema,
    status_code=status.HTTP_200_OK,
)
async def update_program(program_id: int, program_dto: ProgramCreateUpdateSchema):
    try:
        async with database.session() as session:
            updated_program = await programs_repo.update_program(
                session=session,
                program_id=program_id,
                program=program_dto,
            )
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_program


@program_router.delete(
    "/delete_program/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_program(program_id: int):
    try:
        async with database.session() as session:
            program = await programs_repo.delete_program(session=session, program_id=program_id)
    except NotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return program