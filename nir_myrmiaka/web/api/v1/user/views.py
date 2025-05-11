from fastapi import APIRouter, Depends, status, UploadFile, File

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.services.auth.auth_service import UserService
from nir_myrmiaka.services.notify.notify_service import NotificationService
from nir_myrmiaka.web.api.v1.schemas import UserUpdateRequest
from nir_myrmiaka.services.work_managment.file_service import BaseFileService
from nir_myrmiaka.services.work_managment.submission_topic_service import (
    SubmissionTopicService,
)

from nir_myrmiaka.web.api.v1.exc import raise_http_error_from_exception

from .schemas import (
    InfoResponse,
    AllTeachersResponse,
    AllStudentsResponse,
    SetInfoResponse,
    UserNotificationResponseModel,
)

router = APIRouter()


@router.get(
    "/{user_id}/info",
    status_code=status.HTTP_200_OK,
    response_model=InfoResponse,
)
async def get_info_user(
    user_id: int, container: Container = Depends(init_container)
):
    user_service: UserService = container.resolve(UserService)

    try:
        data = await user_service.get_user_info(user_id)
        return InfoResponse(data=data)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get(
    "/{user_id}/notifications",
    status_code=status.HTTP_200_OK,
    response_model=UserNotificationResponseModel,
)
async def get_user_notifications(
    user_id: int, container: Container = Depends(init_container)
):
    notification_service: NotificationService = container.resolve(
        NotificationService
    )

    count, values = await notification_service.get_notifications_by_user_id(
        user_id=user_id
    )

    try:
        return UserNotificationResponseModel(count=count, values=values)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.patch("/set-info", status_code=status.HTTP_201_CREATED)
async def set_info_user(
    payload: UserUpdateRequest,
    container: Container = Depends(init_container),
):
    user_service: UserService = container.resolve(UserService)

    try:
        await user_service.set_user_info(payload.model_dump())
        return SetInfoResponse(data=None)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get(
    "/all-teachers",
    status_code=status.HTTP_200_OK,
    response_model=AllTeachersResponse,
)
async def get_all_teachers(container: Container = Depends(init_container)):
    user_service: UserService = container.resolve(UserService)

    try:
        count, values = await user_service.get_all_teachers()
        return AllTeachersResponse(
            count=count,
            values=values,
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get(
    "/all-students",
    status_code=status.HTTP_200_OK,
    response_model=AllStudentsResponse,
)
async def get_all_students(container: Container = Depends(init_container)):
    user_service: UserService = container.resolve(UserService)

    try:
        count, values = await user_service.get_all_students()
        return AllStudentsResponse(
            count=count,
            values=values,
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.post("/upload")
async def upload_file(
    submission_topic_id: int,
    file: UploadFile = File(...),
    container: Container = Depends(init_container),
):
    submission_topic_service: SubmissionTopicService = container.resolve(
        SubmissionTopicService
    )

    try:
        return await submission_topic_service.upload_related_file(
            submission_topic_id=submission_topic_id, file=file
        )
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.get("/download/{file_id}")
async def get_file(
    file_id: int,
    container: Container = Depends(init_container),
):
    base_file_service: BaseFileService = container.resolve(BaseFileService)

    try:
        return await base_file_service.get_file_by_id(file_id)
    except ValueError as e:
        raise_http_error_from_exception(e)


@router.delete("/remove-file/")
async def remove_file(
    file_id: int,
    container: Container = Depends(init_container),
):
    base_file_service: BaseFileService = container.resolve(BaseFileService)

    try:
        return await base_file_service.delete_file(file_id)
    except ValueError as e:
        raise_http_error_from_exception(e)
