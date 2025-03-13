from pydantic import BaseModel, Field
from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    UsernameField,
    UserUpdateRequest,
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


class UserCreateRequest(RegisterEssentials, UserUpdateRequest): ...


class AuthUserResponseModel(BaseModel):
    id: int
    username: str
    email: Optional[str]

    class Config:
        from_attributes = True


class RegisterResponse(GenericResponse[AuthUserResponseModel]): ...


class LoginResponse(GenericResponse[AuthUserResponseModel]): ...
