from nir_myrmiaka.db.models.users_group import UsersGroup
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class UsersGroupRepository(ExtendedCRUDRepository[UsersGroup]):
    def __init__(self, session):
        super().__init__(session, UsersGroup)
