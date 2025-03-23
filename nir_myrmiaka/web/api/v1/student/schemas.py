from pydantic import BaseModel, Field
from nir_myrmiaka.web.api.v1.schemas import (
    GenericResponse,
    GenericListResponse,
    AssignmentResponseModel,
    IdField,
    PlainCommentModel,
)


class AssignmentTeacherField(IdField): ...


class AssignmentStudentField(IdField): ...


class AssignmentCreateRequest(BaseModel):
    student: AssignmentStudentField
    teacher: AssignmentTeacherField

    text: str = Field(None)


class AssignmentResponse(GenericResponse[AssignmentResponseModel]): ...


class ReviewedCommentsReponse(GenericResponse[PlainCommentModel]): ...
