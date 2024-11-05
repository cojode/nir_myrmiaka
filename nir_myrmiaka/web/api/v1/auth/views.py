from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.dependencies import (
    get_db_session, get_auth_user_repository, get_users_userprofile_repository
)
from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.web.api.v1.schemas import UserCreateRequest



from nir_myrmiaka.settings import settings

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreateRequest,
    db: AsyncSession = Depends(get_db_session)
):
    user_service = UserService(db, 
                               get_auth_user_repository(), 
                               get_users_userprofile_repository())
    
    try:
        user = await user_service.register_user(payload)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db_session)
):
    user_service = UserService(db, 
                               get_auth_user_repository(), 
                               get_users_userprofile_repository())
    
    try:
        await user_service.login_user(username, password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    
