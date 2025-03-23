from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services import SubmissionService, SubmissionTopicService
from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

from .schemas import GetSubmissionResponse, SubmissionTopicsResponse

router = APIRouter()


@router.get(
    "/{submission_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetSubmissionResponse,
)
async def get_submission(
    submission_id: int, container: Container = Depends(init_container)
):
    submission_service: SubmissionService = container.resolve(
        SubmissionService
    )

    try:
        return GetSubmissionResponse(
            data=await submission_service.get_submission_by_id(
                submission_id=submission_id
            )
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get(
    "/{submission_id}/topics",
    status_code=status.HTTP_200_OK,
    response_model=SubmissionTopicsResponse,
)
async def get_submission_topics(
    submission_id: int,
    container: Container = Depends(init_container),
):
    submission_topics_service: SubmissionTopicService = container.resolve(
        SubmissionTopicService
    )

    try:
        count, submissions = (
            await submission_topics_service.get_submission_topics_by_submission_id(
                submission_id=submission_id
            )
        )
        return SubmissionTopicsResponse(count=count, values=submissions)

    except ValueError as e:
        raise_http_error_from_exception(e)
