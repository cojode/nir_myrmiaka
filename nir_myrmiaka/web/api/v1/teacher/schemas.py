from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    AssignmentResponseModel,
    PlainAssignmentResponseModel,
    IdField,
    PlainUserProfileModel,
)
from pydantic import BaseModel
from typing import Optional
import datetime

class BaseSubmissionResponseModel(BaseModel):
    id: int
    assignment: PlainAssignmentResponseModel
    semester: Optional[int]
    created_at: Optional[datetime.datetime]
    research_work: dict
    submission_topics: list[dict]

    class Config:
        from_attributes = True


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


class CreateSubmissionResponse(
    GenericResponse[BaseSubmissionResponseModel]
): ...
