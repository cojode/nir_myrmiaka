from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from nir_myrmiaka.db.models.student import StudentModel as Student

async def get_student_by_user_id(db: AsyncSession, user_id: int) -> Student | None:
    """
    Get a student by user_id.

    :param db: The database session.
    :param username: The username of the user to retrieve.
    :return: The User instance if found, None otherwise.
    """
    stmt = select(Student).where(Student.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

# async def update_student(db: AsyncSession, student: Student, user_in: UserUpdateRequest) -> User:
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