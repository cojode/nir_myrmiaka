from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    AuthUserResponseModel,
)
from pydantic import BaseModel
from typing import Optional


class InfoResponseModel(BaseModel):
    id: int
    role: str
    middle_name: Optional[str]

    user: AuthUserResponseModel

    class Config:
        from_attributes = True


class InfoResponse(GenericResponse[InfoResponseModel]): ...


class StatusResponseModel(BaseModel):
    status: str


class StatusResponse(GenericResponse[StatusResponseModel]): ...


class AllTeachersResponseModel(BaseModel):
    user_id: int
    role: str
    middle_name: str

    user: AuthUserResponseModel
    class Config:
        from_attributes = True


class AllTeachersResponse(GenericListResponse[AllTeachersResponseModel]): ...
