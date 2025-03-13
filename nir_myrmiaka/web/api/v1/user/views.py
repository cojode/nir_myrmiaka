from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.web.api.v1.schemas import UserUpdateRequest

from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

from .schemas import InfoResponse, StatusResponse, AllTeachersResponse

router = APIRouter()


@router.get(
    "/{user_id}/info",
    status_code=status.HTTP_201_CREATED,
    response_model=InfoResponse,
)
async def get_info_user(
    user_id: int, container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)

    try:

        info = await user_service.get_user_info(user_id)
        return InfoResponse(data=info)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get(
    "/{user_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=StatusResponse,
)
async def get_status_user(
    user_id: str, container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)

    try:
        role = await user_service.get_status(user_id)
        return StatusResponse(data=role)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.post("/set-info", status_code=status.HTTP_200_OK)
async def set_status_user(
    payload: UserUpdateRequest, container: Container = Depends(init_container)
):
    user_service = container.resolve(UserService)

    try:
        return await user_service.set_user_info(payload)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get(
    "/all-teachers",
    status_code=status.HTTP_200_OK,
    response_model=AllTeachersResponse,
)
async def get_all_teachers(container: Container = Depends(init_container)):
    user_service: UserService = container.resolve(UserService)

    try:
        count, values = await user_service.get_all_teachers()
        return AllTeachersResponse(count=count, values=values)
    except ValueError as e:
        raise_http_error_from_exception(e)
