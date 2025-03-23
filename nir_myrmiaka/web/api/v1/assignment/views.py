from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services import SubmissionService, AssignmentService
from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

from .schemas import GetAssignmentResponse, AssignmentSubmissionsResponse

router = APIRouter()


@router.get(
    "/{assignment_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetAssignmentResponse,
)
async def get_assignment(
    assignment_id: int, container: Container = Depends(init_container)
):
    assignment_service: AssignmentService = container.resolve(
        AssignmentService
    )

    try:
        return GetAssignmentResponse(
            data=await assignment_service.get_assignment_by_id(
                assignment_id=assignment_id
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get(
    "/{assignment_id}/submissions",
    status_code=status.HTTP_200_OK,
    response_model=AssignmentSubmissionsResponse,
)
async def get_assignment_submissions(
    assignment_id: int,
    container: Container = Depends(init_container),
):
    submission_service: SubmissionService = container.resolve(
        SubmissionService
    )

    try:
        count, submissions = (
            await submission_service.get_submissions_by_assignment_id(
                assignmnet_id=assignment_id
            )
        )
        return AssignmentSubmissionsResponse(count=count, values=submissions)

    except ValueError as e:
        raise_http_error_from_exception(e)
