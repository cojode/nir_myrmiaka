from nir_myrmiaka.db.models.base_researchwork import BaseResearchwork
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class BaseResearchworkRepository(ExtendedCRUDRepository[BaseResearchwork]):
    def __init__(self, session):
        super().__init__(session, BaseResearchwork)
