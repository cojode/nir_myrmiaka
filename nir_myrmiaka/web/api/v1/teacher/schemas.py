from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    AssignmentResponseModel,
    IdField,
    UserProfileResponseModel,
    SubmissionResponseModel,
    SubmissionTopicResponseModel,
)
from pydantic import BaseModel

class AffectAssignmentRequest(BaseModel):
    teacher: IdField
    assignment_id: int


class BrowseAssignmentsResponse(
    GenericListResponse[AssignmentResponseModel]
): ...


class AcceptAssignmentResponse(GenericResponse[AssignmentResponseModel]): ...


class DeclineAssignmentResponse(GenericResponse[AssignmentResponseModel]): ...

class ReviewAssignmentResponse(GenericResponse[AssignmentResponseModel]): ...

class ListStudentsResponse(GenericListResponse[UserProfileResponseModel]): ...

class CreateSubmissionResponse(GenericResponse[SubmissionResponseModel]): ...


class AffectSubmissionTopicRequest(BaseModel):
    submission_topic_id: int


class AffectSubmissionTopicRequestWithComment(AffectSubmissionTopicRequest):
    comment: str


class AcceptSubmissionTopicResponse(
    GenericResponse[SubmissionTopicResponseModel]
): ...


class DeclineSubmissionTopicResponse(
    GenericResponse[SubmissionTopicResponseModel]
): ...


class ReviewSubmissionTopicResponse(
    GenericResponse[SubmissionTopicResponseModel]
): ...
