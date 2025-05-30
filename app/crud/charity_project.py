from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list:
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 1)
        )
        rated_projects = []
        projects = projects.scalars().all()
        for project in projects:
            current_project = []
            current_project.append(project.name)
            current_project.append(project.close_date - project.create_date)
            current_project.append(project.description)
            rated_projects.append(current_project)
        rated_projects.sort(key=lambda rate: rate[1])
        return rated_projects


charity_project_crud = CRUDCharityProject(CharityProject)
