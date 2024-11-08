from nir_myrmiaka.db.models.users_userprofile import UsersUserprofile
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository

class UsersUserprofileRepository(ExtendedCRUDRepository[UsersUserprofile]):
    def __init__(self, session):
        super().__init__(session, UsersUserprofile)