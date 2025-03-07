from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    AssignmentWithStatusResponseModel,
)
from pydantic import BaseModel
from typing import Optional
import datetime

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


class DeclineAssignmentResponse(
    GenericResponse[AssignmentWithStatusResponseModel]
): ...


class BrowseAssignmentsResponse(
    GenericListResponse[AssignmentWithStatusResponseModel]
): ...
