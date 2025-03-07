from pydantic import BaseModel, Field, computed_field
from nir_myrmiaka.web.api.v1.schemas import GenericResponse

from typing import Optional

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


class StatusAssignmentModel(BaseModel):
    is_accepted: Optional[bool]
    is_reviewed: Optional[bool]

    @computed_field
    @property
    def status(self) -> str:
        if not self.is_reviewed:
            return "Не просмотрено"
        if not self.is_accepted:
            return "Отказано"
        return "Принято"

    class Config:
        from_attributes = True


class StatusAssignmentResponse(GenericResponse[StatusAssignmentModel]): ...
