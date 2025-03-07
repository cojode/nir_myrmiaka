from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.work_managment.work_management_service import (
    WorkManagementService,
)

from .schemas import (
    BrowseAssignmentsResponse,
    AcceptAssignmentResponse,
    DeclineAssignmentResponse,
)

from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

router = APIRouter()


@router.get(
    "/browse-assignments",
    status_code=status.HTTP_200_OK,
    response_model=BrowseAssignmentsResponse,
)
async def browse_assignments(
    teacher_id: int, container: Container = Depends(init_container)
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
    )

    try:
        count, values = await work_management_service.browse_assignments(
            teacher_id
        )
        return BrowseAssignmentsResponse(count=count, values=values)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.post(
    "/accept_assignment",
    status_code=status.HTTP_201_CREATED,
    response_model=AcceptAssignmentResponse,
)
async def accept_assignment(
    teacher_id: int,
    semester: int,
    assignment_id: int,
    container: Container = Depends(init_container),
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
    )

    try:
        data = await work_management_service.accept_assignment(
            teacher_id, semester, assignment_id
        )
        return AcceptAssignmentResponse(data=data)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch(
    "/decline_assignment",
    status_code=status.HTTP_200_OK,
    response_model=DeclineAssignmentResponse,
)
async def decline_assignment(
    teacher_id: int,
    assignment_id: int,
    container: Container = Depends(init_container),
):
    work_management_service: WorkManagementService = container.resolve(
        WorkManagementService
    )

    try:
        data = await work_management_service.decline_assignment(
            teacher_id, assignment_id
        )
        return DeclineAssignmentResponse(data=data)
    except ValueError as e:
        raise_http_error_from_exception(e)
