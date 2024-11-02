from fastapi import APIRouter, HTTPException, Depends, status


from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.dependencies import get_db_session
from nir_myrmiaka.db.repositories.users import (
    get_user_by_username, update_user_from_request
)

from nir_myrmiaka.web.api.v1.user.schemas.requests import UserUpdateRequest

router = APIRouter()

@router.get("/{username}", status_code=status.HTTP_200_OK)
async def get_whole_user(
        username: str,
        db: AsyncSession = Depends(get_db_session),
    ):
    """
    Get whole user information from database(for testing purposes)
    If user not found returns 404.
    """
    existing_user = await get_user_by_username(db, username)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such username')

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
    Allowed fields: user_id, status.
    """
    existing_user = await get_user_by_username(db, username)
    allowed = ['user_id', 'status']
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such username')
    if field not in allowed:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Field not allowed')
    return {f"{field}": existing_user.__dict__[field]}

@router.post("/update", status_code=status.HTTP_200_OK)
async def update_user(
        user_in: UserUpdateRequest,
        db: AsyncSession = Depends(get_db_session),
    ):
    """
    Get custom field of a user based on its username.
    If user not found returns 404.
    If field is unknown or prohibited returns 422.
    Allowed fields: user_id, status.
    """
    existing_user = await get_user_by_username(db, user_in.username)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such username')
    return await update_user_from_request(db, existing_user, user_in)
