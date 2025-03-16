from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    PlainUserProfileResponseModel,
)
from pydantic import BaseModel
from typing import Optional


class InfoResponseModel(PlainUserProfileResponseModel): ...


class InfoResponse(GenericResponse[InfoResponseModel]): ...


class StatusResponseModel(BaseModel):
    status: Optional[str]


class StatusResponse(GenericResponse[StatusResponseModel]): ...


class SetInfoResponseModel(BaseModel): ...


class SetInfoResponse(GenericResponse[SetInfoResponseModel]): ...


class AllTeachersResponse(
    GenericListResponse[PlainUserProfileResponseModel]
): ...
