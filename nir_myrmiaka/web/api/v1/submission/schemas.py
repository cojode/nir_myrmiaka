from nir_myrmiaka.web.api.v1.schemas import (
    GenericListResponse,
    GenericResponse,
    SubmissionResponseModel,
    SubmissionTopicResponseModel,
)


class GetSubmissionResponse(GenericResponse[SubmissionResponseModel]): ...


class SubmissionTopicsResponse(
    GenericListResponse[SubmissionTopicResponseModel]
): ...
