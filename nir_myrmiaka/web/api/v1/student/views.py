from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)

from nir_myrmiaka.services.work_managment.comment_service import (
    SubmissionTopicCommentService,
)

from .schemas import (
    AssignmentCreateRequest,
    AssignmentResponse,
    ReviewedCommentsReponse,
)

from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

router = APIRouter()


@router.post(
    "/create-assignment",
    status_code=status.HTTP_201_CREATED,
    response_model=AssignmentResponse,
)
async def create_assignment(
    payload: AssignmentCreateRequest, container: Container = Depends(init_container)
):
    work_management_service: AssignmentService = container.resolve(
        AssignmentService
    )

    try:
        return AssignmentResponse(
            data=await work_management_service.create_assignment(
                student_user_id=payload.student.user_id,
                teacher_user_id=payload.teacher.user_id,
                text=payload.text,
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch(
    "/review-submission-topic-comments",
    status_code=status.HTTP_200_OK,
    response_model=ReviewedCommentsReponse,
)
async def review_submission_topic_comments(
    submission_id: int,
    container: Container = Depends(init_container),
):
    comment_service: SubmissionTopicCommentService = container.resolve(
        SubmissionTopicCommentService
    )
    try:
        count, data = (
            await comment_service.review_comments_by_submission_topic_id(
                submission_id=submission_id
            )
        )
        return ReviewedCommentsReponse(count=count, data=data)
    except ValueError as e:
        raise_http_error_from_exception(e)
