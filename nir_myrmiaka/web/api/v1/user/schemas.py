from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    UserProfileResponseModel,
)
from pydantic import BaseModel
from typing import Optional


class InfoResponseModel(UserProfileResponseModel): ...


class InfoResponse(GenericResponse[InfoResponseModel]): ...


class StatusResponseModel(BaseModel):
    status: Optional[str]


class StatusResponse(GenericResponse[StatusResponseModel]): ...


class SetInfoResponseModel(BaseModel): ...


class SetInfoResponse(GenericResponse[SetInfoResponseModel]): ...


class AllTeachersResponse(GenericListResponse[UserProfileResponseModel]): ...
