from fastapi import APIRouter, HTTPException, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.web.api.v1.schemas import UserUpdateRequest

router = APIRouter()

@router.get("/{username}/info", status_code=status.HTTP_201_CREATED)
async def get_info_user(
    username: str,
    container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)
    
    try:
        info = await user_service.get_user_info(username)
        return info
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{username}/status", status_code=status.HTTP_200_OK)
async def get_status_user(
    username: str,
    container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)
    
    try:
        role = await user_service.get_status(username)
        return role
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/set-info", status_code=status.HTTP_200_OK)
async def set_status_user(
    payload: UserUpdateRequest,
    container: Container = Depends(init_container)
):
    user_service = container.resolve(UserService)
    
    try:
        await user_service.set_user_info(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/all-teachers", status_code=status.HTTP_200_OK)
async def get_all_teachers(container: Container = Depends(init_container)):
    user_service: UserService = container.resolve(UserService)
    
    try:
        return await user_service.get_all_teachers()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


    

