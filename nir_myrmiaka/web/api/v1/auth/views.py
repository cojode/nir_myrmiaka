from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

from .schemas import RegisterResponse, LoginResponse, UserCreateRequest

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
)
async def register_user(
    payload: UserCreateRequest, container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)

    try:
        auth_user, user_profile = await user_service.register_user(
            auth_data=payload.auth.model_dump(),
            user_profile_data=payload.user_profile.model_dump(),
            essentials=payload.essentials.model_dump(),
        )
        return RegisterResponse(
            data={"user": auth_user, "profile": user_profile}
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginResponse
)
async def login_user(
    username: str, password: str, container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)

    try:
        auth_user = await user_service.login_user(username, password)
        return LoginResponse(data={"user": auth_user})

    except ValueError as e:
        raise_http_error_from_exception(e)
