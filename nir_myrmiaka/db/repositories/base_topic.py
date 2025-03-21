from nir_myrmiaka.db.models.base_topic import BaseTopic
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class BaseTopicRepository(ExtendedCRUDRepository[BaseTopic]):
    def __init__(self, session):
        super().__init__(session, BaseTopic)
