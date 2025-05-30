from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_closed_project, check_name_duplicate,
                                check_new_full_amount, check_project_exists,
                                check_project_with_donation)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import get_donations_for_project

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создает новый благотворительный проект.

    Доступно только для суперпользователей.

    Проверяет, что имя проекта уникально, создает проект,
    затем обновляет информацию о проекте с учетом текущих пожертвований.

    """
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    project_after_investing = await get_donations_for_project(
        new_project, session
    )
    return project_after_investing


@router.get(
    "/", response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получает список всех благотворительных проектов.
    """
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Частично обновляет данные благотворительного проекта.

    Доступно только для суперпользователей.

    Проверяет существование проекта, что он не закрыт,
    проверяет уникальность нового имени и корректность новой суммы,
    затем обновляет проект.
    """
    charity_project = await check_project_exists(project_id, session)
    await check_closed_project(project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_new_full_amount(obj_in.full_amount, project_id, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет благотворительный проект.

    Доступно только для суперпользователей.

    Проверяет существование проекта и отсутствие связанных пожертвований,
    затем удаляет проект из базы данных.

    """
    charity_project = await check_project_exists(project_id, session)
    await check_project_with_donation(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
