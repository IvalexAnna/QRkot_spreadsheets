from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

from . import constants


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.ERR_NAME_DUPLICATE,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=constants.ERR_PROJECT_NOT_FOUND
        )
    return project


async def check_project_with_donation(
        project_id: int, session: AsyncSession
) -> None:
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.ERR_PROJECT_WITH_DONATION,
        )


async def check_closed_project(project_id: int, session: AsyncSession) -> None:
    project = await charity_project_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.ERR_CLOSED_PROJECT_EDIT,
        )


async def check_new_full_amount(
    new_full_amount: int, project_id: int, session: AsyncSession
) -> None:
    project = await charity_project_crud.get(project_id, session)
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.ERR_AMOUNT_LESS_THAN_INVESTED,
        )
