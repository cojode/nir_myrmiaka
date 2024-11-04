from nir_myrmiaka.db.models.auth_user import AuthUser
from nir_myrmiaka.db.repositories.base_crud import BaseCRUD

class AuthUserRepository(BaseCRUD[AuthUser]):
    def __init__(self):
        super().__init__(AuthUser)