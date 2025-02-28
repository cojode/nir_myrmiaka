from pydantic import BaseModel, Field, EmailStr
from typing import Optional, TypeVar, Generic

T = TypeVar("T")

"""
Generic or common schemas for endpoints
"""


class GenericResponse(BaseModel, Generic[T]):
    msg: str = Field(default="success", example="success")
    data: Optional[T]


class DictResponse(GenericResponse[dict]): ...


class UsernameField(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class UserUpdateRequest(UsernameField):
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=254)
    middle_name: Optional[str] = Field(None, max_length=30)
    group_id: Optional[int] = Field(None)
