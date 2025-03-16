from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    computed_field,
    field_validator,
)
from typing import Optional, TypeVar, Generic
import datetime

T = TypeVar("T")

"""
Generic or common schemas for endpoints
"""


class GenericResponseMessageField(BaseModel):
    msg: str = Field(default="success", example="success")


class GenericResponse(GenericResponseMessageField, Generic[T]):
    data: Optional[T]


class GenericListResponse(GenericResponseMessageField, Generic[T]):
    count: int
    values: list[T]


class UsernameField(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class IdField(BaseModel):
    user_id: int = Field()


class AuthUserResponseModel(BaseModel):
    id: int
    username: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        from_attributes = True


class UserProfileResponseModel(BaseModel):
    middle_name: Optional[str]
    group_id: Optional[int]
    role: Optional[str]

    class Config:
        from_attributes = True


class AuthUserInfoResponseModel(BaseModel):
    user: Optional[AuthUserResponseModel]


class FullUserInfoResponseModel(AuthUserInfoResponseModel):
    profile: Optional[UserProfileResponseModel]


class UserProfileRequestModel(BaseModel):
    middle_name: Optional[str] = Field(None, max_length=30)
    group_id: Optional[int] = Field(None)


class AuthUserRequestModel(BaseModel):
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=254)


class HeadlessUserUpdateRequest(BaseModel):
    auth: AuthUserRequestModel
    user_profile: UserProfileRequestModel


class UserUpdateRequest(BaseModel):
    target: IdField
    data: HeadlessUserUpdateRequest


class ComputedAssignmentStatus(BaseModel):
    @computed_field
    @property
    def status(self) -> str:
        if not self.is_reviewed:
            return "Не просмотрено"
        if not self.is_accepted:
            return "Отказано"
        return "Принято"

    class Config:
        from_attributes = True


class AssignmentResponseModel(BaseModel):
    id: int
    text: str
    is_accepted: Optional[bool]
    is_reviewed: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class AssignmentWithStudentProfileResponseModel(AssignmentResponseModel):
    user: UserProfileResponseModel


class StatusedAssignmentResponseModel(
    AssignmentResponseModel, ComputedAssignmentStatus
): ...
