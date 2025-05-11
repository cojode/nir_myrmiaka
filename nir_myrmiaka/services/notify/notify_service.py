from nir_myrmiaka.db.models.notification import (
    NotificationType,
    NotificationEntityModelType,
)

from nir_myrmiaka.db.repositories.notification import (
    NotificationRepository,
    Notification,
)
from nir_myrmiaka.db.repositories.notification_entity import (
    NotificationEntityRepository,
    NotificationEntity,
)

from nir_myrmiaka.db.database import Database

from nir_myrmiaka.services.common.crud_service import BaseCRUDService


class NotificationEntityService(BaseCRUDService[NotificationEntity]):
    def __init__(self, db: Database):
        super().__init__(db, NotificationEntityRepository)

    async def append_notification_entity(
        self,
        notification_id: int,
        entity_model: NotificationEntityModelType,
        entity_id: int,
    ) -> dict:
        """Creates a new notification entity."""
        return await self._create_model(
            notification_id=notification_id,
            entity_model=entity_model,
            entity_id=entity_id,
        )


class NotificationService(BaseCRUDService[Notification]):

    def __init__(
        self,
        db: Database,
        notification_entity_service: NotificationEntityService,
    ):
        super().__init__(db, NotificationRepository)
        self.notification_entity_service = notification_entity_service

    async def dismiss_notification(self, notification_id: int) -> dict:
        return await self._update_model(notification_id, is_read=True)

    async def notify_user(
        self,
        user_id: int,
        notification_type: NotificationType,
        message: str,
        related_entities: list[tuple[NotificationEntityModelType, int]],
    ) -> dict:
        """Creates a new notification for a user."""
        notification = await self._create_model(
            user_id=user_id,
            type=notification_type,
            message=message,
        )
        for entity_model, entity_id in related_entities:
            await self.notification_entity_service.append_notification_entity(
                notification_id=notification.get("id"),
                entity_model=entity_model,
                entity_id=entity_id,
            )

        return await self._get_model_by_id(notification.get("id"))

    async def get_notifications_by_user_id(
        self, user_id: int
    ) -> tuple[int, list[dict]]:
        """Fetches all notifications for a user."""
        notifications = await self._search_model_by_fields(user_id=user_id)
        return len(notifications), notifications
