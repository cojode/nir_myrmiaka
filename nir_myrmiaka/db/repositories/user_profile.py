from nir_myrmiaka.db.models.user_profile import UserProfile
from nir_myrmiaka.db.repositories.crud import ExtendedCRUDRepository


class UserProfileRepository(ExtendedCRUDRepository[UserProfile]):
    def __init__(self, session):
        super().__init__(session, UserProfile)
