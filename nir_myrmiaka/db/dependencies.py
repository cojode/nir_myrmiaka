from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from nir_myrmiaka.db.repositories.auth_user import AuthUserRepository
from nir_myrmiaka.db.repositories.users_userprofile import UsersUserprofileRepository


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:
        yield session
    finally:
        await session.commit()
        await session.close()

def get_auth_user_repository() -> AuthUserRepository:
    return AuthUserRepository()

def get_users_userprofile_repository() -> UsersUserprofileRepository:
    return UsersUserprofileRepository()