from fastapi import APIRouter, HTTPException, Depends, status


from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.repositories.users import (
    get_user_by_username
)

from nir_myrmiaka.db.repositories.student import (
    get_student_by_user_id, get_student_by_username, create_student
)

from nir_myrmiaka.db.dependencies import get_db_session

router = APIRouter()

@router.get("/{username}", status_code=status.HTTP_200_OK)
async def get_whole_student(
        username: str,
        db: AsyncSession = Depends(get_db_session),
    ):
    """
    Get whole user information from database(for testing purposes)
    If user not found returns 404.
    """
    existing_user = await get_student_by_username(db, username)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such username')
    
    existing_user.user_id

    return existing_user.__dict__

@router.get("/{username}/{field}", status_code=status.HTTP_200_OK)
async def get_user_field(
        username: str,
        field: str,
        db: AsyncSession = Depends(get_db_session),
    ):
    """
    Get custom field of a user based on its username.
    If user not found returns 404.
    If field is unknown or prohibited returns 422.
    Allowed fields: ['task_id', 'number_group']
    """
    existing_user = await get_student_by_username(db, username)
    allowed = ['task_id', 'number_group']
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such username')
    if field not in allowed:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Field not allowed')
    return {f"{field}": existing_user.__dict__[field]}

@router.post("/update", status_code=status.HTTP_200_OK)
async def update_student(
        user_in, # StudentUpdateRequest,
        db: AsyncSession = Depends(get_db_session)
    ):
    pass
    """
    Update user fields
    """