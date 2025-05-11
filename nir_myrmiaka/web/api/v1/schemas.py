from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Optional, TypeVar, Generic
from enum import Enum
from fastapi.encoders import jsonable_encoder
import datetime

from nir_myrmiaka.log import logger

import json

T = TypeVar("T")

"""
Generic or common schemas for endpoints
"""

class GenericResponseMessageField(BaseModel):
    msg: str = Field(default="success", example="success")


class ApplicationErrorResponse(GenericResponseMessageField):
    error: Enum
    msg: str = Field(default="error", example="error")
    detail: Optional[dict] = Field(None)


class ServiceOutputLoggerMixin:
    def __init__(self, **kwargs):
        logger.debug("Attempting to return response with service output: ")
        logger.debug(
            f"\n{json.dumps(jsonable_encoder(kwargs), indent=4, sort_keys=True, ensure_ascii=False)}"
        )
        super().__init__(**kwargs)


class GenericResponse(
    GenericResponseMessageField, ServiceOutputLoggerMixin, Generic[T]
):
    data: Optional[T]


class GenericListResponse(
    GenericResponseMessageField, ServiceOutputLoggerMixin, Generic[T]
):
    count: int
    values: list[T]


class UsernameField(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class StudentTeacherIdField(BaseModel):
    student_id: int
    teacher_id: int


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


class PlainAssignmentResponseModel(
    BaseAssignmentResponseModel, StudentTeacherIdField
): ...


class HeadlessUserProfileModel(BaseModel, from_attributes=True):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    about_me: Optional[str] = None
    group_id: Optional[int] = None


class UserUpdateRequest(BaseModel):
    target: IdField
    data: HeadlessUserProfileModel
    zalupa: Optional[bool] = False

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
    submission_title: str
    created_at: Optional[datetime.datetime]


class PlainSubmissionModel(BaseSubmissionModel, StudentTeacherIdField):
    assignment_id: int
    researchwork_id: int


class AssignmentResponseModel(BaseAssignmentResponseModel):
    student: Optional[PlainUserProfileModel]
    teacher: Optional[PlainUserProfileModel]
    submissions: list[PlainSubmissionModel]


class PlainGroupModel(BaseModel):
    id: int
    group_name: str


class NotificationEntityModel(BaseModel):
    id: int
    entity_id: int
    entity_model: Enum


class BaseNotificationModel(BaseModel):
    id: int
    user_id: int
    type: Enum
    message: str
    created_at: datetime.datetime
    is_read: bool


class PlainNotificationModel(BaseNotificationModel): ...


class NotificationResponseModel(BaseNotificationModel):
    entities: Optional[list[NotificationEntityModel]]


class UserProfileResponseModel(BaseUserProfileModel):
    group: Optional[PlainGroupModel]
    notifications: Optional[list[BaseNotificationModel]]
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


class BaseCommentModel(BaseModel):
    id: int
    comment: Optional[str]
    is_reviewed: bool
    created_at: Optional[datetime.datetime]


class PlainCommentModel(BaseCommentModel):
    submission_topic_id: int


class BaseSubmissionTopicModel(BaseModel):
    id: int
    is_accepted: Optional[bool]
    is_reviewed: Optional[bool]


class PlainSubmissionTopicModel(
    BaseSubmissionTopicModel,
):
    submission_id: int
    topic_id: int


class SubmissionTopicResponseModel(BaseSubmissionTopicModel):
    submission: PlainSubmissionModel
    topic: PlainTopicModel
    comments: list[PlainCommentModel]
    files: list[dict]


class CommentResponseModel(BaseCommentModel):
    topic_submission: PlainSubmissionTopicModel


class SubmissionResponseModel(BaseSubmissionModel):
    submission_topics: list[PlainSubmissionTopicModel]
    assignment: PlainAssignmentResponseModel
    research_work: PlainResearchworkModel

    @computed_field
    @property
    def is_accepted(self) -> bool:
        return all(st.is_accepted for st in self.submission_topics[1:])

    @computed_field
    @property
    def is_reviewed(self) -> bool:
        return all(st.is_reviewed for st in self.submission_topics[1:])


class UserGroupsModel(BaseModel):
    id: int
    group_name: str
