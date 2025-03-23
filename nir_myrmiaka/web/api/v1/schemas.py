from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    computed_field,
)
from typing import Optional, TypeVar, Generic
import datetime

from nir_myrmiaka.log import logger

T = TypeVar("T")

"""
Generic or common schemas for endpoints
"""


class GenericResponseMessageField(BaseModel):
    msg: str = Field(default="success", example="success")

    def __init__(self, **kwargs):
        logger.info(
            f"Attempting to return response with service output: {kwargs}"
        )
        super().__init__(**kwargs)


class GenericResponse(GenericResponseMessageField, Generic[T]):
    data: Optional[T]


class GenericListResponse(GenericResponseMessageField, Generic[T]):
    count: int
    values: list[T]


class UsernameField(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class IdField(BaseModel):
    user_id: int = Field()

class UserProfileRequestModel(BaseModel):
    middle_name: Optional[str] = Field(None, max_length=30)
    group_id: Optional[int] = Field(None)


class AuthUserRequestModel(BaseModel):
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=254)


class HeadlessUserUpdateRequest(
    AuthUserRequestModel, UserProfileRequestModel
): ...


class BaseAssignmentResponseModel(BaseModel, from_attributes=True):
    id: int
    text: str
    is_accepted: Optional[bool]
    is_reviewed: bool
    created_at: datetime.datetime

    @computed_field
    @property
    def status(self) -> str:
        if not self.is_reviewed:
            return "Не просмотрено"
        if not self.is_accepted:
            return "Отказано"
        return "Принято"


class PlainAssignmentResponseModel(BaseAssignmentResponseModel):
    student_id: int
    teacher_id: int


class HeadlessUserProfileModel(BaseModel, from_attributes=True):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    group_id: Optional[int] = None


class UserUpdateRequest(BaseModel):
    target: IdField
    data: HeadlessUserProfileModel


class BaseUserProfileModel(HeadlessUserProfileModel):
    id: int
    username: str
    date_joined: Optional[datetime.datetime]
    last_login: Optional[datetime.datetime]
    role: Optional[str]


class PlainUserProfileModel(BaseUserProfileModel):
    group_id: Optional[int]


class BaseSubmissionModel(BaseModel):
    id: int
    semester: Optional[int]
    created_at: Optional[datetime.datetime]


class PlainSubmissionModel(BaseSubmissionModel):
    assignment_id: int
    researchwork_id: int


class AssignmentResponseModel(BaseAssignmentResponseModel):
    student: Optional[PlainUserProfileModel]
    teacher: Optional[PlainUserProfileModel]
    submissions: list[PlainSubmissionModel]


class PlainGroupModel(BaseModel):
    id: int
    group_name: str


class UserProfileResponseModel(BaseUserProfileModel):

    group: Optional[PlainGroupModel]
    assignment_subordinate: Optional[list[PlainAssignmentResponseModel]]
    assignment_supervisor: Optional[list[PlainAssignmentResponseModel]]

    @computed_field
    @property
    def last_accepted_assignment_subordinate(
        self,
    ) -> Optional[PlainAssignmentResponseModel]:
        if not self.assignment_subordinate:
            return
        for assignment in self.assignment_subordinate[::-1]:
            if assignment.is_accepted == True:
                return assignment

    @computed_field
    @property
    def last_accepted_assignment_supervisor(
        self,
    ) -> Optional[PlainAssignmentResponseModel]:
        if not self.assignment_supervisor:
            return
        for assignment in self.assignment_supervisor[::-1]:
            if assignment.is_accepted == True:
                return assignment


class BaseResearchworkModel(BaseModel):
    id: int
    name: str
    description: str


class PlainResearchworkModel(BaseResearchworkModel): ...


class BaseTopicModel(BaseModel):
    id: int
    name: str


class PlainTopicModel(BaseTopicModel):
    research_work_id: int


class BaseSubmissionTopicModel(BaseModel):
    id: int
    comment: Optional[str]
    is_accepted: Optional[bool]
    is_reviewed: Optional[bool]


class PlainSubmissionTopicModel(BaseSubmissionTopicModel):
    submission_id: int
    topic_id: int


class SubmissionTopicResponseModel(BaseSubmissionTopicModel):
    submission: PlainSubmissionModel
    topic: PlainTopicModel
    files: list[dict]


class SubmissionResponseModel(BaseSubmissionModel):
    submission_topics: list[PlainSubmissionTopicModel]
    assignment: PlainAssignmentResponseModel
    research_work: PlainResearchworkModel

    @computed_field
    @property
    def is_accepted(self) -> bool:
        for st in self.submission_topics:
            if not st.is_accepted:
                return False
        return True
