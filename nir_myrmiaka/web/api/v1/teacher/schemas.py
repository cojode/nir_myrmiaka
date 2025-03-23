from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    AssignmentResponseModel,
    IdField,
    PlainUserProfileModel,
    SubmissionResponseModel,
)
from pydantic import BaseModel

class AffectAssignmentRequest(BaseModel):
    teacher: IdField
    assignment_id: int


class AcceptAssignmentResponse(GenericResponse[AssignmentResponseModel]): ...


class BrowseAssignmentsResponse(
    GenericListResponse[AssignmentResponseModel]
): ...


class DeclineAssignmentResponse(GenericResponse[AssignmentResponseModel]): ...

class ReviewAssignmentResponse(GenericResponse[AssignmentResponseModel]): ...

class ListStudentsResponse(GenericListResponse[PlainUserProfileModel]): ...


class CreateSubmissionResponse(GenericResponse[SubmissionResponseModel]): ...
