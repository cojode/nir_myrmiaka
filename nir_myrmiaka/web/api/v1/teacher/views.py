from fastapi import APIRouter, HTTPException, Depends, status


from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.repositories.teacher import (
    get_teacher_by_username, all_teachers
)

from nir_myrmiaka.db.dependencies import get_db_session

router = APIRouter()

@router.get("/all_teachers", status_code=status.HTTP_200_OK)
async def get_all_teachers(
        db: AsyncSession = Depends(get_db_session)
    ):
    """
    Get all teachers available
    """
    teachers = await all_teachers(db)
    return {"teachers": teachers}

@router.get("/{username}", status_code=status.HTTP_200_OK)
async def get_whole_teacher(
        username: str,
        db: AsyncSession = Depends(get_db_session),
    ):
    """
    Get whole user information from database(for testing purposes)
    If user not found returns 404.
    """
    existing_user = await get_teacher_by_username(db, username)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such username')

    return existing_user.__dict__

@router.get("/{username}/{field}", status_code=status.HTTP_200_OK)
async def get_teacher_field(
        username: str,
        field: str,
        db: AsyncSession = Depends(get_db_session),
    ):
    """
    Get custom field of a user based on its username.
    If user not found returns 404.
    If field is unknown or prohibited returns 422.
    Allowed fields: []
    """
    existing_user = await get_teacher_by_username(db, username)
    allowed = []
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such username')
    if field not in allowed:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Field not allowed')
    return {f"{field}": existing_user.__dict__[field]}