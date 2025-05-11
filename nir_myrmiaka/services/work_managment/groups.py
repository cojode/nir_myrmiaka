from nir_myrmiaka.db.database import Database

from nir_myrmiaka.db.repositories.user_group import (
    UsersGroupRepository,
    UsersGroup,
)

from nir_myrmiaka.services.common.crud_service import BaseCRUDService


class UsersGroupService(BaseCRUDService[UsersGroup]):
    def __init__(self, db: Database):
        super().__init__(db, UsersGroupRepository)

    async def get_all_groups(self) -> tuple[int, dict]:
        groups = await self._list_all_models()
        return len(groups), groups
