from pydantic import BaseModel, Field
from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    AssignmentResponseModel,
    IdField,
)


class AssignmentTeacherField(IdField): ...


class AssignmentStudentField(IdField): ...


class AssignmentCreateRequest(BaseModel):
    student: AssignmentStudentField
    teacher: AssignmentTeacherField

    text: str = Field(None)


class AssignmentResponse(GenericResponse[AssignmentResponseModel]): ...
