from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.web.api.v1.schemas import UserCreateRequest



from nir_myrmiaka.settings import settings

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreateRequest,
    container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)
    
    try:
        user = await user_service.register_user(payload)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    username: str,
    password: str,
    container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)
    
    try:
        await user_service.login_user(username, password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    
