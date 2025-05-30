from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    """
    Базовая модель пожертвования с основными полями.
    """

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """
    Модель для создания нового пожертвования.
    """

    pass


class UserDonationDB(DonationBase):
    """
    Модель пожертвования для пользователя с доп. полями из базы данных.
    """

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(UserDonationDB):
    """
    Модель пожертвования с информацией о статусе и связью с пользователем.
    """

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
