from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from nir_myrmiaka.db.models.teacher import TeacherModel as Teacher
from nir_myrmiaka.db.models.users import UsersModel as User

async def get_teacher_by_user_id(db: AsyncSession, user_id: int) -> Teacher | None:
    """
    Get a teacher by user_id.

    :param db: The database session.
    :param user_id: The user_id of the user to retrieve.
    :return: The User instance if found, None otherwise.
    """
    stmt = select(Teacher).where(Teacher.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_teacher_by_username(db: AsyncSession, username: str) -> Teacher | None:
    """
    Get a teacher by username.

    :param db: The database session.
    :param username: The username of the user to retrieve.
    :return: The User instance if found, None otherwise.
    """
    stmt = (select(Teacher)
            .join(User, Teacher.user_id == User.user_id)
            .where(User.username == username))
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_teacher_from_request(db: AsyncSession, teacher: Teacher, teacher_in) -> Teacher:
    """
    Update user information.

    :param db: The database session.
    :param user: The User instance to update.
    :param user_in: The UserUpdateRequest containing updated details.
    :return: The updated User instance.
    """
    for key, value in teacher_in.__dict__.items():
        if value is not None:
            setattr(teacher, key, value)

    await db.commit()
    await db.refresh(teacher)
    return teacher

async def create_teacher(db: AsyncSession, user_id: int) -> Teacher:
    """
    Create a new user.

    :param db: The database session.
    :param user_in: The UserCreateRequest containing user details.
    :return: The created User instance.
    """
    
    db_teacher = Teacher(
        user_id=user_id
    )
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)
    return db_teacher

async def all_teachers(db: AsyncSession) -> list[Teacher]:
    stmt = select(Teacher)
    result = await db.execute(stmt)
    return list(result.scalars().all())