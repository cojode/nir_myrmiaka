from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from nir_myrmiaka.db.models.users import UsersModel as User
from nir_myrmiaka.web.api.v1.auth.schemas.requests import UserCreateRequest
from nir_myrmiaka.services.auth.security import hash_password

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

# async def update_user(db: AsyncSession, user: User, user_in: UserUpdateRequest) -> User:
#     """
#     Update user information.

#     :param db: The database session.
#     :param user: The User instance to update.
#     :param user_in: The UserUpdateRequest containing updated details.
#     :return: The updated User instance.
#     """
#     if user_in.email is not None:
#         user.email = user_in.email
#     if user_in.username is not None:
#         user.username = user_in.username
#     if user_in.callsign is not None:
#         user.callsign = user_in.callsign
#     if user_in.full_name is not None:
#         user.full_name = user_in.full_name
#     if user_in.password is not None:
#         user.password_hash = hash_password(user_in.password)
#     await db.commit()
#     await db.refresh(user)
#     return user

# async def delete_user(db: AsyncSession, user: User) -> None:
#     """
#     Delete a user.

#     :param db: The database session.
#     :param user: The User instance to delete.
#     """
#     await db.delete(user)
#     await db.commit()