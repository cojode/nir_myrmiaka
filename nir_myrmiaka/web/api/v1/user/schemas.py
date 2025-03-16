from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    FullUserInfoResponseModel,
)
from pydantic import BaseModel


class InfoResponseModel(FullUserInfoResponseModel): ...


class InfoResponse(GenericResponse[InfoResponseModel]): ...


class StatusResponseModel(BaseModel):
    status: str


class StatusResponse(GenericResponse[StatusResponseModel]): ...


class SetInfoResponseModel(BaseModel): ...


class SetInfoResponse(GenericResponse[SetInfoResponseModel]): ...


class AllTeachersResponse(GenericListResponse[FullUserInfoResponseModel]): ...
