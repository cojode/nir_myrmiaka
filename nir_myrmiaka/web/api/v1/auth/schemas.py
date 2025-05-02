from pydantic import BaseModel, Field
from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    UsernameField,
    HeadlessUserUpdateRequest,
    UserProfileRequestModel,
    UserProfileResponseModel,
)
from typing import Optional


class PasswordMixinSchema(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters long.",
    )


class RegisterEssentials(PasswordMixinSchema, UsernameField): ...


class LoginEssentials(UsernameField, PasswordMixinSchema): ...


class UserProfileCreateRequestModel(HeadlessUserUpdateRequest):
    role: Optional[str] = Field(max_length=20)


class UserCreateRequest(UserProfileCreateRequestModel, RegisterEssentials): ...


class RegisterResponse(GenericResponse[UserProfileResponseModel]): ...


class LoginResponse(GenericResponse[UserProfileResponseModel]): ...
