from pydantic import BaseModel, Field
from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    UsernameField,
    HeadlessUserUpdateRequest,
    AuthUserResponseModel,
)
from typing import Optional


class PasswordMixinSchema(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters long.",
    )


class RegisterEssentials(PasswordMixinSchema, UsernameField):
    role: Optional[str] = Field(max_length=20)


class UserCreateRequest(RegisterEssentials, HeadlessUserUpdateRequest): ...


class RegisterResponse(GenericResponse[AuthUserResponseModel]): ...


class LoginResponse(GenericResponse[AuthUserResponseModel]): ...
