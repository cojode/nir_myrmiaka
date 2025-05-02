from nir_myrmiaka.db.models.notification import NotificationType

from nir_myrmiaka.db.repositories.notification import (
    NotificationRepository,
    Notification,
)
from nir_myrmiaka.db.database import Database

from nir_myrmiaka.services.common.crud_service import BaseCRUDService


class NotificationService(BaseCRUDService[Notification]):
    def __init__(self, db: Database):
        super().__init__(db, NotificationRepository)

    async def notify_user(
        self,
        user_id: int,
        notification_type: NotificationType,
        message: str,
        related_entity_id: int,
    ) -> Notification:
        """Creates a new notification for a user."""
        notification = await self._create_model(
            user_id=user_id,
            type=notification_type,
            message=message,
            related_entity_id=related_entity_id,
        )
        return notification
