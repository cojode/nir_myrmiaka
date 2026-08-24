from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services import (
    SubmissionService,
    SubmissionTopicService,
    SubmissionTopicCommentService,
)

from .schemas import (
    GetSubmissionResponse,
    SubmissionTopicsResponse,
    EditSubmissionRequest,
    EditSubmissionResponse,
    CreateCommentRequest,
    EditCommentRequest,
    CommentResponse,
    CommentsListResponse,
)

router = APIRouter()


@router.get(
    "/{submission_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetSubmissionResponse,
)
async def get_submission(
    submission_id: int, container: Container = Depends(init_container)
):
    submission_service: SubmissionService = container.resolve(
        SubmissionService
    )

    return GetSubmissionResponse(
        data=await submission_service.get_submission_by_id(
            submission_id=submission_id
        )
    )


@router.patch(
    "/{submission_id}",
    status_code=status.HTTP_200_OK,
    response_model=EditSubmissionResponse,
)
async def edit_submission(
    payload: EditSubmissionRequest,
    container: Container = Depends(init_container),
):
    submission_service: SubmissionService = container.resolve(
        SubmissionService
    )

    return GetSubmissionResponse(
        data=await submission_service.edit_submission_by_id(
            submission_id=payload.submission_id,
            submission_title=payload.submission_title,
            researchwork_id=payload.researchwork_id,
        )
    )


@router.get(
    "/{submission_id}/topics",
    status_code=status.HTTP_200_OK,
    response_model=SubmissionTopicsResponse,
)
async def get_submission_topics(
    submission_id: int,
    container: Container = Depends(init_container),
):
    submission_topics_service: SubmissionTopicService = container.resolve(
        SubmissionTopicService
    )

    count, submissions = (
        await submission_topics_service.get_submission_topics_by_submission_id(
            submission_id=submission_id
        )
    )
    return SubmissionTopicsResponse(count=count, values=submissions)


@router.post(
    "/topic/{submission_topic_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
)
async def create_comment(
    submission_topic_id: int,
    payload: CreateCommentRequest,
    container: Container = Depends(init_container),
):
    comment_service: SubmissionTopicCommentService = container.resolve(
        SubmissionTopicCommentService
    )
    return CommentResponse(
        data=await comment_service.create_comment(
            comment=payload.comment,
            submission_topic_id=submission_topic_id,
            user_id=payload.user_id,
        )
    )


@router.get(
    "/topic/{submission_topic_id}/comments",
    status_code=status.HTTP_200_OK,
    response_model=CommentsListResponse,
)
async def get_comments(
    submission_topic_id: int,
    container: Container = Depends(init_container),
):
    comment_service: SubmissionTopicCommentService = container.resolve(
        SubmissionTopicCommentService
    )
    count, values = await comment_service.get_comments_by_submission_topic_id(
        submission_topic_id=submission_topic_id
    )
    return CommentsListResponse(count=count, values=values)


@router.patch(
    "/topic/comments/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def edit_comment(
    comment_id: int,
    payload: EditCommentRequest,
    container: Container = Depends(init_container),
):
    comment_service: SubmissionTopicCommentService = container.resolve(
        SubmissionTopicCommentService
    )
    return CommentResponse(
        data=await comment_service.update_comment(
            comment_id=comment_id,
            user_id=payload.user_id,
            new_text=payload.comment,
        )
    )


@router.delete(
    "/topic/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment_id: int,
    user_id: int,
    container: Container = Depends(init_container),
):
    comment_service: SubmissionTopicCommentService = container.resolve(
        SubmissionTopicCommentService
    )
    await comment_service.delete_comment(
        comment_id=comment_id,
        user_id=user_id,
    )
