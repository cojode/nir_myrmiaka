from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from nir_myrmiaka.db.models.users import UsersModel as User
from nir_myrmiaka.services.auth.security import verify_password


async def authenticate_user(db: AsyncSession, login: str, password: str):
    stmt = select(User).where(
        (User.login == login)
    )
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user or not verify_password(password, user.password):
        return None
    return user