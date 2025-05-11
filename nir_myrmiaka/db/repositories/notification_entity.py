from nir_myrmiaka.db.models.notification import NotificationEntity
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class NotificationEntityRepository(ExtendedCRUDRepository[NotificationEntity]):
    def __init__(self, session):
        super().__init__(session, NotificationEntity)
