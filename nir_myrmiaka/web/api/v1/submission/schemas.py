from pydantic import BaseModel

from nir_myrmiaka.web.api.v1.schemas import (
    GenericListResponse,
    GenericResponse,
    SubmissionResponseModel,
    SubmissionTopicResponseModel,
    PlainCommentModel,
)


class GetSubmissionResponse(GenericResponse[SubmissionResponseModel]): ...


class EditSubmissionResponse(GenericResponse[SubmissionResponseModel]): ...


class EditSubmissionRequest(BaseModel):
    submission_id: int
    submission_title: str | None
    researchwork_id: int | None


class SubmissionTopicsResponse(
    GenericListResponse[SubmissionTopicResponseModel]
): ...


class CreateCommentRequest(BaseModel):
    submission_topic_id: int
    user_id: int
    comment: str


class EditCommentRequest(BaseModel):
    user_id: int
    comment: str


class CommentResponse(GenericResponse[PlainCommentModel]): ...


class CommentsListResponse(GenericListResponse[PlainCommentModel]): ...
