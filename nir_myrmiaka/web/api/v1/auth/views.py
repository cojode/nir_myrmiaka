from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.services.auth.cas_service import CasService

from .schemas import (
    RegisterResponse,
    LoginResponse,
    UserCreateRequest,
    LoginEssentials,
    CasLoginRequest,
)

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
    user_profile = await user_service.register_user(payload.model_dump())
    return RegisterResponse(data=user_profile)


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginResponse
)
async def login_user(
    payload: LoginEssentials, container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)

    user_profile = await user_service.login_user(
        payload.username, payload.password
    )
    return LoginResponse(data=user_profile)


@router.post(
    "/cas/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
)
async def cas_login_user(
    payload: CasLoginRequest,
    container: Container = Depends(init_container),
) -> LoginResponse:
    """Authenticate a user via CAS ticket.

    The backend calls CAS /serviceValidate with the ticket to verify
    the user's identity, then finds or creates the corresponding user.
    """
    cas_service: CasService = container.resolve(CasService)
    user_profile = await cas_service.cas_login(
        ticket=payload.ticket,
        service_path=payload.service,
    )
    return LoginResponse(data=user_profile)


@router.get(
    "/cas/callback",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def cas_callback() -> HTMLResponse:
    """CAS callback endpoint for Android WebView interception.

    This endpoint deliberately does NOT call serviceValidate —
    the Android app intercepts the redirect and extracts the ticket
    before calling POST /cas/login. Calling serviceValidate here
    would consume the ticket, causing the actual login to fail.

    Returns a simple HTML page instructing the user to close the window.
    """
    html_content = (
        "<html><head><meta charset='utf-8'></head>"
        "<body><p>Можно закрыть окно</p></body>"
        "</html>"
    )
    return HTMLResponse(content=html_content)
