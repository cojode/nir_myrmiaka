from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
)
from pydantic import BaseModel, computed_field
from typing import Optional
import datetime


class AssignmentResponseModel(BaseModel):
    id: int
    created_at: datetime.datetime
    text: str
    is_accepted: bool
    is_reviewed: bool

    class Config:
        from_attributes = True


class BaseSubmissionResponseModel(BaseModel):
    id: int
    assignment_id: int
    semester: int
    created_at: datetime.datetime
    research_work_id: Optional[int]

    class Config:
        from_attributes = True


class AcceptAssignmentResponse(
    GenericResponse[BaseSubmissionResponseModel]
): ...


class DeclineAssignmentResponse(GenericResponse[AssignmentResponseModel]): ...


class BrowseAssignmentsResponse(
    GenericListResponse[AssignmentResponseModel]
): ...
