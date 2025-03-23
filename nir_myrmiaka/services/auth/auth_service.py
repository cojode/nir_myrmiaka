from nir_myrmiaka.db.models.user_profile import UserProfile

from nir_myrmiaka.db.repositories.user_profile import UserProfileRepository

from nir_myrmiaka.services.auth.security import hash_password, verify_password

from nir_myrmiaka.db.database import Database

from nir_myrmiaka.services.common.crud_service import BaseCRUDService

from typing import Dict, Any, List


from datetime import datetime


class UserService(BaseCRUDService[UserProfile]):
    def __init__(self, db: Database):
        super().__init__(db, UserProfileRepository)

    @staticmethod
    def _extract_from_payload(
        payload: Dict[str, Any], *args: str
    ) -> Dict[str, Any]:
        """Extracts specified keys from a payload dictionary."""
        return {key: payload[key] for key in args if key in payload}

    async def register_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Registers a new user."""
        existing_user = await self.repo.find_one(username=data["username"])
        if existing_user:
            raise ValueError("Username already taken")

        data["password"] = hash_password(data["password"])
        data["last_login"] = data["date_joined"] = datetime.now()

        new_user = await self._create_model(**data)
        return new_user

    async def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticates and logs in a user."""
        user = await self.repo.find_one(username=username)
        if not user or not verify_password(password, user.password):
            raise ValueError("Invalid credentials")

        user.last_login = datetime.now()
        saved_user = await self.repo.save(user)
        return saved_user.to_dict()

    async def get_user_info(self, user_id: int) -> Dict[str, Any]:
        """Gets detailed information about a user."""
        return await self._get_model_by_id(user_id)

    async def get_all_teachers(self) -> tuple[int, List[Dict[str, Any]]]:
        """Gets all users with the 'Teacher' role."""
        teachers = await self.repo.find_all(role="Teacher")
        return len(teachers), [teacher.to_dict() for teacher in teachers]

    async def set_user_info(self, payload: Dict[str, Any]) -> None:
        """Updates user information."""
        target_id = payload["target"]["user_id"]
        await self._get_model_by_id(target_id)  # Verify user exists
        await self.repo.update_by_filter(fields=payload["data"], id=target_id)

    async def verify_exists_and_role_specified(
        self, user_id: int, role: str
    ) -> dict[str, Any]:
        """Verifies that a user exists and has the specified role."""
        user = await self._get_model_by_id(user_id)
        if user.get("role", None) != role:
            raise ValueError(
                f"User with ID {user_id} does not have the specified role ({role})"
            )
        return user
