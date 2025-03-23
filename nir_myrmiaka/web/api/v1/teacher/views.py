from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)

from nir_myrmiaka.services.work_managment.submission_service import (
    SubmissionService,
)

from nir_myrmiaka.services.work_managment.submission_topic_service import (
    SubmissionTopicService,
)

from .schemas import (
    AcceptAssignmentResponse,
    DeclineAssignmentResponse,
    ReviewAssignmentResponse,
    AffectAssignmentRequest,
    ListStudentsResponse,
    CreateSubmissionResponse,
    AffectSubmissionTopicRequest,
    AffectSubmissionTopicRequestWithComment,
    AcceptSubmissionTopicResponse,
    DeclineSubmissionTopicResponse,
    ReviewSubmissionTopicResponse,
)

from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

router = APIRouter()


@router.get(
    "/list-students",
    status_code=status.HTTP_200_OK,
    response_model=ListStudentsResponse,
)
async def list_students(
    teacher_id: int,
    container: Container = Depends(init_container),
):
    work_management_service: AssignmentService = container.resolve(
        AssignmentService
    )
    try:
        count, values = await work_management_service.get_accepted_students(
            teacher_id=teacher_id
        )
        return ListStudentsResponse(count=count, values=values)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch(
    "/accept-assignment",
    status_code=status.HTTP_200_OK,
    response_model=AcceptAssignmentResponse,
)
async def accept_assignment(
    payload: AffectAssignmentRequest,
    container: Container = Depends(init_container),
):
    work_management_service: AssignmentService = container.resolve(
        AssignmentService
    )
    try:
        return AcceptAssignmentResponse(
            data=await work_management_service.accept_assignment(
                payload.teacher.user_id, payload.assignment_id
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch(
    "/decline-assignment",
    status_code=status.HTTP_200_OK,
    response_model=DeclineAssignmentResponse,
)
async def decline_assignment(
    payload: AffectAssignmentRequest,
    container: Container = Depends(init_container),
):
    work_management_service: AssignmentService = container.resolve(
        AssignmentService
    )

    try:
        return DeclineAssignmentResponse(
            data=await work_management_service.decline_assignment(
                payload.teacher.user_id, payload.assignment_id
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch(
    "/review-assignment",
    status_code=status.HTTP_200_OK,
    response_model=DeclineAssignmentResponse,
)
async def review_assignment(
    payload: AffectAssignmentRequest,
    container: Container = Depends(init_container),
):
    work_management_service: AssignmentService = container.resolve(
        AssignmentService
    )

    try:
        return ReviewAssignmentResponse(
            data=await work_management_service.review_assignment(
                payload.teacher.user_id, payload.assignment_id
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.post(
    "/create-submission",
    status_code=status.HTTP_200_OK,
    response_model=CreateSubmissionResponse,
)
async def create_submission(
    assignment_id: int,
    researchwork_id: int,
    submission_title: str,
    container: Container = Depends(init_container),
):
    submission_service: SubmissionService = container.resolve(
        SubmissionService
    )

    try:
        submission = await submission_service.create_submission(
            assignment_id=assignment_id,
            researchwork_id=researchwork_id,
            submission_title=submission_title,
        )
        return CreateSubmissionResponse(data=submission)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch(
    "/accept-submission-topic",
    status_code=status.HTTP_200_OK,
    response_model=AcceptSubmissionTopicResponse,
)
async def accept_submission_topic(
    payload: AffectSubmissionTopicRequestWithComment,
    container: Container = Depends(init_container),
):
    work_management_service: SubmissionTopicService = container.resolve(
        SubmissionTopicService
    )
    try:
        return AcceptSubmissionTopicResponse(
            data=await work_management_service.accept_submission_topic(
                payload.submission_topic_id, payload.comment
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch(
    "/decline-submission-topic",
    status_code=status.HTTP_200_OK,
    response_model=DeclineSubmissionTopicResponse,
)
async def decline_submission_topic(
    payload: AffectSubmissionTopicRequestWithComment,
    container: Container = Depends(init_container),
):
    work_management_service: SubmissionTopicService = container.resolve(
        SubmissionTopicService
    )

    try:
        return DeclineSubmissionTopicResponse(
            data=await work_management_service.decline_submission_topic(
                payload.submission_topic_id, payload.comment
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch(
    "/review-submission-topic",
    status_code=status.HTTP_200_OK,
    response_model=DeclineSubmissionTopicResponse,
)
async def review_submission_topic(
    payload: AffectSubmissionTopicRequest,
    container: Container = Depends(init_container),
):
    work_management_service: SubmissionTopicService = container.resolve(
        SubmissionTopicService
    )

    try:
        return ReviewSubmissionTopicResponse(
            data=await work_management_service.review_submission_topic(
                payload.submission_topic_id
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)
