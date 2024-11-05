from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.dependencies import (
    get_db_session, get_auth_user_repository, get_users_userprofile_repository
)
from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.web.api.v1.schemas import UserUpdateRequest

from nir_myrmiaka.settings import settings

router = APIRouter()

@router.get("/{username}/info", status_code=status.HTTP_201_CREATED)
async def register_user(
    username: str,
    db: AsyncSession = Depends(get_db_session)
):
    user_service = UserService(db, 
                               get_auth_user_repository(), 
                               get_users_userprofile_repository())
    
    try:
        info = await user_service.get_user_info(username)
        return info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{username}/status", status_code=status.HTTP_200_OK)
async def status_user(
    username: str,
    db: AsyncSession = Depends(get_db_session)
):
    user_service = UserService(db, 
                               get_auth_user_repository(), 
                               get_users_userprofile_repository())
    
    try:
        role = await user_service.get_status(username)
        return role
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/set-info", status_code=status.HTTP_200_OK)
async def status_user(
    payload: UserUpdateRequest,
    db: AsyncSession = Depends(get_db_session)
):
    user_service = UserService(db, 
                               get_auth_user_repository(), 
                               get_users_userprofile_repository())
    
    try:
        await user_service.set_user_info(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    

