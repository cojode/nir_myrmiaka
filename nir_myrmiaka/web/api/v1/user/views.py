from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.web.api.v1.schemas import UserUpdateRequest

from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

import json

from .schemas import (
    InfoResponse,
    AllTeachersResponse,
    AllStudentsResponse,
    SetInfoResponse,
)

router = APIRouter()


@router.get(
    "/{user_id}/info",
    status_code=status.HTTP_200_OK,
    response_model=InfoResponse,
)
async def get_info_user(
    user_id: int, container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)

    try:
        data = await user_service.get_user_info(user_id)
        print(data)
        return InfoResponse(data=data)
    except ValueError as e:
        raise_http_error_from_exception(e)

@router.patch("/set-info", status_code=status.HTTP_201_CREATED)
async def set_info_user(
    payload: UserUpdateRequest,
    container: Container = Depends(init_container),
):
    user_service: UserService = container.resolve(UserService)

    try:
        await user_service.set_user_info(payload.model_dump())
        return SetInfoResponse(data=None)
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
        return AllTeachersResponse(
            count=count,
            values=values,
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get(
    "/all-students",
    status_code=status.HTTP_200_OK,
    response_model=AllStudentsResponse,
)
async def get_all_students(container: Container = Depends(init_container)):
    user_service: UserService = container.resolve(UserService)

    try:
        count, values = await user_service.get_all_students()
        return AllStudentsResponse(
            count=count,
            values=values,
        )
    except ValueError as e:
        raise_http_error_from_exception(e)
