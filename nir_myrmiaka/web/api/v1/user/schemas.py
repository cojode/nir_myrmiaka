from nir_myrmiaka.web.api.v1.schemas import GenericResponse, DictResponse
from pydantic import BaseModel, EmailStr
from typing import Optional


class InfoResponseModel(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    group: Optional[int]


class InfoResponse(GenericResponse[InfoResponseModel]): ...


class StatusResponseModel(BaseModel):
    status: str


class StatusResponse(GenericResponse[StatusResponseModel]): ...


class AllTeachersResponseModel(BaseModel): ...


class AllTeachersResponse(DictResponse): ...
