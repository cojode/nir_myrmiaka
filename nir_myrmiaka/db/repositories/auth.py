from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from nir_myrmiaka.db.models.users import UsersModel as User
from nir_myrmiaka.services.auth.security import verify_password, hash_password

from nir_myrmiaka.web.api.v1.auth.schemas.requests import UserCreateRequest

async def authenticate_user(db: AsyncSession, username: str, password: str):
    stmt = select(User).where(
        (User.username == username)
    )
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user or not verify_password(password, user.password):
        return None
    return user

async def create_user(db: AsyncSession, user_in: UserCreateRequest) -> User:
    """
    Create a new user.

    :param db: The database session.
    :param user_in: The UserCreateRequest containing user details.
    :return: The created User instance.
    """
    
    db_user = User(
        username=user_in.username,
        password=hash_password(user_in.password),
        status=user_in.status
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user