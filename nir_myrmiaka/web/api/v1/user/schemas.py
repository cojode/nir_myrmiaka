from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
)
from pydantic import BaseModel, EmailStr
from typing import Optional


class InfoResponseModel(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    group: Optional[int]


class InfoResponse(GenericResponse[InfoResponseModel]): ...


class StatusResponseModel(BaseModel):
    status: str


class StatusResponse(GenericResponse[StatusResponseModel]): ...


class AllTeachersResponseModel(BaseModel):
    user_id: int
    role: str
    middle_name: str

    class Config:
        from_attributes = True


class AllTeachersResponse(GenericListResponse[AllTeachersResponseModel]): ...
