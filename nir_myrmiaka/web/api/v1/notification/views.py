from fastapi import APIRouter, Depends, status

from punq import Container
from nir_myrmiaka.container.container import init_container

from nir_myrmiaka.exceptions.abc import DomainError

from nir_myrmiaka.services.notify.notify_service import NotificationService

from nir_myrmiaka.web.api.v1.schemas import (
    NotificationResponseModel,
    GenericResponse,
)


class NotificationResponse(GenericResponse[NotificationResponseModel]): ...


router = APIRouter()


@router.patch(
    "/dismiss",
    status_code=status.HTTP_200_OK,
    response_model=NotificationResponse,
)
async def dismiss_notification(
    notification_id: int, container: Container = Depends(init_container)
):
    notification_service: NotificationService = container.resolve(
        NotificationService
    )
    data = await notification_service.dismiss_notification(notification_id)
    raise DomainError(
        message="Notification not found",
        detail=f"Notification with id {notification_id} not found",
    )
    return NotificationResponse(data=data)
