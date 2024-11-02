from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from nir_myrmiaka.db.models.users import UsersModel as User

# from nir_myrmiaka.web.api.v1.user.schemas.requests import UserUpdateRequest


async def update_user_from_request(db: AsyncSession, user: User, user_in) -> User:
    """
    Update user information.

    :param db: The database session.
    :param user: The User instance to update.
    :param user_in: The UserUpdateRequest containing updated details.
    :return: The updated User instance.
    """
    for key, value in user_in.__dict__.items():
        if value is not None:
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """
    Get a user by username.

    :param db: The database session.
    :param username: The username of the user to retrieve.
    :return: The User instance if found, None otherwise.
    """
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Get a user by ID.

    :param db: The database session.
    :param user_id: The ID of the user to retrieve.
    :return: The User instance if found, None otherwise.
    """
    stmt = select(User).where(User.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def delete_user(db: AsyncSession, user: User) -> None:
    """
    Delete a user.

    :param db: The database session.
    :param user: The User instance to delete.
    """
    await db.delete(user)
    await db.commit()