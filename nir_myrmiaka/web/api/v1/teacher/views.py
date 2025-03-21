from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
)

from .schemas import (
    AcceptAssignmentResponse,
    DeclineAssignmentResponse,
    ReviewAssignmentResponse,
    AffectAssignmentRequest,
    ListStudentsResponse,
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
        count, values = (
            await work_management_service.get_accepted_students_plain(
                teacher_id=teacher_id
            )
        )
        return ListStudentsResponse(count=count, values=values)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.post(
    "/accept-assignment",
    status_code=status.HTTP_201_CREATED,
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
