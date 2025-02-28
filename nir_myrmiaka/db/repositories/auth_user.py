from nir_myrmiaka.db.models.auth_user import AuthUser
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class AuthUserRepository(ExtendedCRUDRepository[AuthUser]):
    def __init__(self, session):
        super().__init__(session, AuthUser)
