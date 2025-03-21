from nir_myrmiaka.db.database import Database

from nir_myrmiaka.db.repositories.base_researchwork import (
    BaseResearchworkRepository,
    BaseResearchwork,
)


class ResearchworkService:

    def __init__(
        self,
        db: Database,
    ):
        self.db = db
        self.base_researchwork_repo = BaseResearchworkRepository(session=db)

    async def get_researchwork_by_id(self, researchwork_id: int) -> dict:
        return await self.base_researchwork_repo.find_by_id(
            researchwork_id
        ).to_dict()

    async def verify_researchwork_id_exists(
        self, researchwork_id: int
    ) -> dict:
        target_researchwork = await self.get_researchwork_by_id(
            researchwork_id=researchwork_id
        )
        if not target_researchwork:
            raise ValueError(
                f"Researchwork with provided id [{researchwork_id}] does not exists."
            )
        return target_researchwork

    async def list_researchworks(self) -> list[dict]:
        return await [
            item.to_dict()
            for item in await self.base_researchwork_repo.find_all()
        ]
