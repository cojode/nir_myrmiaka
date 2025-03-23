from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    AssignmentResponseModel,
    SubmissionResponseModel,
)


class GetAssignmentResponse(GenericResponse[AssignmentResponseModel]): ...


class AssignmentSubmissionsResponse(
    GenericListResponse[SubmissionResponseModel]
): ...
