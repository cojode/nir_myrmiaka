from nir_myrmiaka.db.models.users_userprofile import UsersUserprofile
from nir_myrmiaka.db.repositories.base_crud import BaseCRUD

class UsersUserprofileRepository(BaseCRUD[UsersUserprofile]):
    def __init__(self):
        super().__init__(UsersUserprofile)