from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services.work_managment.work_management_service import (
    WorkManagementService,
)

from .schemas import (
    AssignmentCreateRequest,
    AssignmentResponse,
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
    work_management_service = container.resolve(WorkManagementService)

    try:
        info = await work_management_service.create_assignment(payload)
        print(info)
        return AssignmentResponse(data=info)
    except ValueError as e:
        raise_http_error_from_exception(e)
