from pydantic import BaseModel, Field
from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    UsernameField,
    HeadlessUserUpdateRequest,
    AuthUserResponseModel,
    UserProfileRequestModel,
    AuthUserRequestModel,
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


class UserProfileCreateRequestModel(UserProfileRequestModel):
    role: Optional[str] = Field(max_length=20)


class UserCreateRequest(HeadlessUserUpdateRequest):
    auth: Optional[AuthUserRequestModel]
    user_profile: Optional[UserProfileCreateRequestModel]
    essentials: RegisterEssentials


class RegisterResponse(GenericResponse[AuthUserResponseModel]): ...


class LoginResponse(GenericResponse[AuthUserResponseModel]): ...
