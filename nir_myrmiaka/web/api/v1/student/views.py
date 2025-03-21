from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services.work_managment.assignment_service import (
    AssignmentService,
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
