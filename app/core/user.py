
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate
from .config import logger


PASSWORD_LENGTH = 3


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Асинхронный генератор
    Предоставляет объект базы данных пользователей.
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """
    Возвращает стратегию JWT для аутентификации.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Валидация пароля и обработка событий регистрации.
    """

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """
        Проверяет корректность пароля пользователя.
        """
        if len(password) < PASSWORD_LENGTH:
            logger.warning(
                f"Cлишком короткий пароль для пользователя {user.email}"
            )
            raise InvalidPasswordException(
                reason=(
                    f"Пароль должен иметь минимум {PASSWORD_LENGTH} символов"
                )
            )
        if user.email in password:
            logger.warning(f"Пароль содержит e-mail пользователя {user.email}")
            raise InvalidPasswordException(
                reason="Пароль не должен совпадать с email"
            )

        logger.debug(f"Пароль для пользователя {user.email} прошёл валидацию")

    async def on_after_register(
            self, user: User,
            request: Optional[Request] = None
    ):
        """
        Обработчик события после успешной регистрации пользователя.
        Выводит в лог сообщение о регистрации.
        """
        logger.info(f"Пользователь {user.email} зарегистрирован.")


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Асинхронный генератор, предоставляющий экземпляр UserManager.
    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
