from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    computed_field,
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

class UserProfileRequestModel(BaseModel):
    middle_name: Optional[str] = Field(None, max_length=30)
    group_id: Optional[int] = Field(None)


class AuthUserRequestModel(BaseModel):
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=254)


class HeadlessUserUpdateRequest(
    AuthUserRequestModel, UserProfileRequestModel
): ...


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
    student: Optional[dict]
    teacher: Optional[dict]

    class Config:
        from_attributes = True


class StatusedAssignmentResponseModel(
    AssignmentResponseModel, ComputedAssignmentStatus
): ...


class HeadlessPlainUserProfileModel(BaseModel, from_attributes=True):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    group_id: Optional[int]


class PlainUserProfileResponseModel(HeadlessPlainUserProfileModel):
    id: int
    username: str
    group: Optional[dict]
    role: Optional[str]
    date_joined: Optional[datetime.datetime]
    last_login: Optional[datetime.datetime]
    assignment_subordinate: Optional[list[dict]]
    assignment_supervisor: Optional[list[dict]]


class UserUpdateRequest(BaseModel):
    target: IdField
    data: HeadlessPlainUserProfileModel
