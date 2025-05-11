from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container
from nir_myrmiaka.services import SubmissionService, SubmissionTopicService

from .schemas import (
    GetSubmissionResponse,
    SubmissionTopicsResponse,
    EditSubmissionRequest,
    EditSubmissionResponse,
)

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

    return GetSubmissionResponse(
        data=await submission_service.get_submission_by_id(
            submission_id=submission_id
        )
    )


@router.patch(
    "/{submission_id}",
    status_code=status.HTTP_200_OK,
    response_model=EditSubmissionResponse,
)
async def edit_submission(
    payload: EditSubmissionRequest,
    container: Container = Depends(init_container),
):
    submission_service: SubmissionService = container.resolve(
        SubmissionService
    )

    return GetSubmissionResponse(
        data=await submission_service.edit_submission_by_id(
            submission_id=payload.submission_id,
            submission_title=payload.submission_title,
            researchwork_id=payload.researchwork_id,
        )
    )


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

    count, submissions = (
        await submission_topics_service.get_submission_topics_by_submission_id(
            submission_id=submission_id
        )
    )
    return SubmissionTopicsResponse(count=count, values=submissions)
