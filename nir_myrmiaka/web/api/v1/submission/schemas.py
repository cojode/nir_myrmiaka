from pydantic import BaseModel

from nir_myrmiaka.web.api.v1.schemas import (
    GenericListResponse,
    GenericResponse,
    SubmissionResponseModel,
    SubmissionTopicResponseModel,
)


class GetSubmissionResponse(GenericResponse[SubmissionResponseModel]): ...


class EditSubmissionResponse(GenericResponse[SubmissionResponseModel]): ...


class EditSubmissionRequest(BaseModel):
    submission_id: int
    submission_title: str | None
    researchwork_id: int | None


class SubmissionTopicsResponse(
    GenericListResponse[SubmissionTopicResponseModel]
): ...
