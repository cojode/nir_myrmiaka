from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Optional, TypeVar, Generic
import datetime

T = TypeVar("T")

"""
Generic or common schemas for endpoints
"""


class GenericResponse(BaseModel, Generic[T]):
    msg: str = Field(default="success", example="success")
    data: Optional[T]


class GenericListResponse(BaseModel, Generic[T]):
    msg: str = Field(default="success", example="success")
    count: int
    values: list[T]


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
    is_accepted: bool
    is_reviewed: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class AssignmentWithStatusResponseModel(
    AssignmentResponseModel, ComputedAssignmentStatus
): ...


class UsernameField(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class UserUpdateRequest(UsernameField):
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=254)
    middle_name: Optional[str] = Field(None, max_length=30)
    group_id: Optional[int] = Field(None)
