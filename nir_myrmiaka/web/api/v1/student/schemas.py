from pydantic import BaseModel, Field
from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    AssignmentWithStatusResponseModel,
)


class AssignmentCreateRequest(BaseModel):
    student_id: int = Field(None)
    teacher_id: int = Field(None)
    text: str = Field(None)


class AssignmentResponse(
    GenericResponse[AssignmentWithStatusResponseModel]
): ...
