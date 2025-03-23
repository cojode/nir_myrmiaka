from nir_myrmiaka.db.database import Database

from nir_myrmiaka.db.repositories.base_researchwork import (
    BaseResearchworkRepository,
    BaseResearchwork,
)

from nir_myrmiaka.services.common.crud_service import BaseCRUDService


class ResearchworkService(BaseCRUDService[BaseResearchwork]):
    def __init__(self, db: Database):
        super().__init__(db, BaseResearchworkRepository)

    async def get_researchwork_by_id(self, researchwork_id: int):
        return await self._get_model_by_id(researchwork_id)
