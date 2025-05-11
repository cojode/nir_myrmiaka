from nir_myrmiaka.db.models.user_profile import UserProfile

from nir_myrmiaka.db.repositories.user_profile import UserProfileRepository

from nir_myrmiaka.services.auth.security import hash_password, verify_password

from nir_myrmiaka.db.database import Database

from nir_myrmiaka.services.common.crud_service import (
    BaseCRUDService,
    EntityNotFoundError,
)

from nir_myrmiaka.exceptions.abc import DomainError, RepositoryError

from typing import Dict, Any, List

from datetime import datetime


class UserServiceError(DomainError):
    """Base exception class for user service errors."""


class UsernameAlreadyTakenError(UserServiceError):
    """Exception raised when a username is already taken."""

    def __init__(self, username: str):
        super().__init__(
            message="Username already taken", detail={"username": username}
        )


class InvalidCredentialsError(UserServiceError):
    """Exception raised when invalid credentials are provided."""

    def __init__(self):
        super().__init__(message="Invalid credentials")


class UserNotFoundError(UserServiceError):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: int):
        super().__init__(message="User not found", detail={"user_id": user_id})


class RoleMismatchError(UserServiceError):
    """Exception raised when a user does not have the specified role."""

    def __init__(self, user_id: int, role: str):
        super().__init__(
            message="User does not have the specified role",
            detail={"user_id": user_id, "role": role},
        )


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
            raise UsernameAlreadyTakenError(data["username"])

        data["password"] = hash_password(data["password"])
        data["last_login"] = data["date_joined"] = datetime.now()

        new_user = await self._create_model(**data)
        return new_user

    async def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticates and logs in a user."""
        user = await self.repo.find_one(username=username)
        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsError

        user.last_login = datetime.now()
        saved_user = await self.repo.save(user)
        return saved_user.to_dict()

    async def get_user_info(self, user_id: int) -> Dict[str, Any]:
        """Gets detailed information about a user."""
        try:
            return await self._get_model_by_id(user_id)
        except EntityNotFoundError as e:
            raise UserNotFoundError(user_id=e.entity_id) from e

    async def get_all_teachers(self) -> tuple[int, List[Dict[str, Any]]]:
        """Gets all users with the 'Teacher' role."""
        teachers = await self.repo.find_all(role="Teacher")
        return len(teachers), [teacher.to_dict() for teacher in teachers]

    async def get_all_students(self) -> tuple[int, List[Dict[str, Any]]]:
        """Gets all users with the 'Student' role."""
        students = await self.repo.find_all(role="Student")
        return len(students), [student.to_dict() for student in students]

    async def set_user_info(self, payload: Dict[str, Any]) -> None:
        """Updates user information."""
        target_id = payload["target"]["user_id"]
        await self._get_model_by_id(target_id)
        await self.repo.update_by_filter(fields=payload["data"], id=target_id)

    async def verify_exists_and_role_specified(
        self, user_id: int, role: str
    ) -> dict[str, Any]:
        """Verifies that a user exists and has the specified role."""
        user = await self._get_model_by_id(user_id)
        if user.get("role", None) != role:
            raise RoleMismatchError(user_id=user_id, role=role)
        return user
