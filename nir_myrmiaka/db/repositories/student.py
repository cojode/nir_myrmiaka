from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from nir_myrmiaka.db.models.student import StudentModel as Student
from nir_myrmiaka.db.models.users import UsersModel as User

async def get_student_by_user_id(db: AsyncSession, user_id: int) -> Student | None:
    """
    Get a student by user_id.

    :param db: The database session.
    :param user_id: The user_id of the user to retrieve.
    :return: The User instance if found, None otherwise.
    """
    stmt = select(Student).where(Student.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_student_by_username(db: AsyncSession, username: str) -> Student | None:
    """
    Get a student by username.

    :param db: The database session.
    :param username: The username of the user to retrieve.
    :return: The User instance if found, None otherwise.
    """
    stmt = (select(Student)
            .join(User, Student.user_id == User.user_id)
            .where(User.username == username))
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_student_from_request(db: AsyncSession, student: Student, student_in) -> Student:
    """
    Update user information.

    :param db: The database session.
    :param user: The User instance to update.
    :param user_in: The UserUpdateRequest containing updated details.
    :return: The updated User instance.
    """
    for key, value in student_in.__dict__.items():
        if value is not None:
            setattr(student, key, value)

    await db.commit()
    await db.refresh(student)
    return student

async def create_student(db: AsyncSession, user_id: int) -> Student:
    """
    Create a new user.

    :param db: The database session.
    :param user_in: The UserCreateRequest containing user details.
    :return: The created User instance.
    """
    
    db_student = Student(
        user_id=user_id
    )
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student