from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services import SubmissionService, AssignmentService

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
    return GetAssignmentResponse(
        data=await assignment_service.get_assignment_by_id(
            assignment_id=assignment_id
        )
    )


@router.delete(
    "/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_assignment(
    assignment_id: int, container: Container = Depends(init_container)
):
    assignment_service: AssignmentService = container.resolve(
        AssignmentService
    )

    await assignment_service.delete_assignment(assignment_id)


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
    count, submissions = (
        await submission_service.get_submissions_by_assignment_id(
            assignmnet_id=assignment_id
        )
    )
    return AssignmentSubmissionsResponse(count=count, values=submissions)
