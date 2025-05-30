from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def make_close_obj(obj):
    obj.close_date = datetime.now()
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    return obj


async def get_projects_for_donation(
    donation: Donation, session: AsyncSession
) -> Donation:
    projects_for_donation = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == 0)
    )
    projects_for_donation = projects_for_donation.scalars().all()
    donation_amount = donation.full_amount
    for project in projects_for_donation:
        entering = donation_amount + project.invested_amount
        if project.full_amount > entering:
            donation = make_close_obj(donation)
            project.invested_amount = entering
            session.add(project)
            break
        elif project.full_amount <= entering:
            donation_amount = entering - project.full_amount
            project = make_close_obj(project)
            session.add(project)
            if donation_amount == 0:
                donation = make_close_obj(donation)
                break
            else:
                donation.invested_amount = donation.full_amount
                - donation_amount
    session.add(donation)
    await session.commit()
    await session.refresh(donation)
    return donation


async def get_donations_for_project(
    project: CharityProject, session: AsyncSession
) -> CharityProject:
    donations_for_project = await session.execute(
        select(Donation).where(Donation.fully_invested == 0)
    )
    donations_for_project = donations_for_project.scalars().all()
    project_amount = project.invested_amount
    for donation in donations_for_project:
        free_donation_amount = donation.full_amount - donation.invested_amount
        new_project_amount = project_amount + free_donation_amount
        if project.full_amount >= new_project_amount:
            donation = make_close_obj(donation)
            project_amount = new_project_amount
            session.add(donation)
            if project_amount == project.full_amount:
                project = make_close_obj(project)
                break
            else:
                project.invested_amount = project_amount
        elif project.full_amount < new_project_amount:
            project = make_close_obj(project)
            donation.invested_amount = donation.full_amount - (
                new_project_amount - project.full_amount
            )
            session.add(donation)
            break
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project
