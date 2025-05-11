from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)

from nir_myrmiaka.services.work_managment.groups import UsersGroupService

from nir_myrmiaka.services.work_managment.comment_service import (
    SubmissionTopicCommentService,
)

from .schemas import (
    AssignmentCreateRequest,
    AssignmentResponse,
    ReviewedCommentsReponse,
    AllGroupsResponse,
)

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
    return AssignmentResponse(
        data=await work_management_service.create_assignment(
            student_user_id=payload.student.user_id,
            teacher_user_id=payload.teacher.user_id,
            text=payload.text,
        )
    )


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
    count, data = await comment_service.review_comments_by_submission_topic_id(
        submission_id=submission_id
    )
    return ReviewedCommentsReponse(count=count, data=data)


@router.get(
    "/list-groups",
    status_code=status.HTTP_200_OK,
    response_model=AllGroupsResponse,
)
async def list_groups(
    container: Container = Depends(init_container),
):
    group_service: UsersGroupService = container.resolve(UsersGroupService)
    count, values = await group_service.get_all_groups()
    return AllGroupsResponse(count=count, values=values)
