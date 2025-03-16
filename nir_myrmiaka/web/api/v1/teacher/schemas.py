from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    StatusedAssignmentResponseModel,
    PlainUserProfileResponseModel,
    IdField,
)
from pydantic import BaseModel
from typing import Optional
import datetime

class BaseSubmissionResponseModel(BaseModel):
    id: int
    assignment_id: int
    semester: Optional[int]
    created_at: Optional[datetime.datetime]
    research_work_id: Optional[int]

    class Config:
        from_attributes = True


class AffectAssignmentRequest(BaseModel):
    teacher: IdField
    assignment_id: int


class AcceptAssignmentResponse(
    GenericResponse[BaseSubmissionResponseModel]
): ...


class StatusedAssignmentWithStudentFullUserInfoModel(BaseModel):
    assignment: Optional[StatusedAssignmentResponseModel]
    student: Optional[PlainUserProfileResponseModel]


class BrowseAssignmentsResponse(
    GenericListResponse[StatusedAssignmentWithStudentFullUserInfoModel]
): ...


class DeclineAssignmentResponse(
    GenericResponse[StatusedAssignmentWithStudentFullUserInfoModel]
): ...


class ReviewAssignmentResponse(
    GenericResponse[StatusedAssignmentWithStudentFullUserInfoModel]
): ...
