from nir_myrmiaka.db.models.notification import Notification
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class NotificationRepository(ExtendedCRUDRepository[Notification]):
    def __init__(self, session):
        super().__init__(session, Notification)
