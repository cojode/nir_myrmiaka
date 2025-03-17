from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.work_managment.work_management_service import (
    WorkManagementService,
)

from .schemas import (
    AcceptAssignmentResponse,
    DeclineAssignmentResponse,
    ReviewAssignmentResponse,
    AffectAssignmentRequest,
)

from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

router = APIRouter()

@router.post(
    "/accept_assignment",
    status_code=status.HTTP_201_CREATED,
    response_model=AcceptAssignmentResponse,
)
async def accept_assignment(
    payload: AffectAssignmentRequest,
    container: Container = Depends(init_container),
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
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
    "/decline_assignment",
    status_code=status.HTTP_200_OK,
    response_model=DeclineAssignmentResponse,
)
async def decline_assignment(
    payload: AffectAssignmentRequest,
    container: Container = Depends(init_container),
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
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
    "/review_assignment",
    status_code=status.HTTP_200_OK,
    response_model=DeclineAssignmentResponse,
)
async def review_assignment(
    payload: AffectAssignmentRequest,
    container: Container = Depends(init_container),
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
    )

    try:
        return ReviewAssignmentResponse(
            data=await work_management_service.review_assignment(
                payload.teacher.user_id, payload.assignment_id
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)
