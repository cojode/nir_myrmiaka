from pydantic import BaseModel, Field
from nir_myrmiaka.web.api.v1.schemas import GenericResponse

import datetime


class AssignmentCreateRequest(BaseModel):
    student_id: int = Field(None)
    teacher_id: int = Field(None)
    text: str = Field(None)


class AssignmentResponseModel(BaseModel):
    text: str
    is_accepted: bool
    is_reviewed: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class AssignmentResponse(GenericResponse[AssignmentResponseModel]): ...
