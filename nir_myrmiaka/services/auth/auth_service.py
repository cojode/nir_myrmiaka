from nir_myrmiaka.db.models.auth_user import AuthUser
from nir_myrmiaka.db.models.users_userprofile import UsersUserprofile

from nir_myrmiaka.db.repositories.auth_user import AuthUserRepository
from nir_myrmiaka.db.repositories.users_userprofile import UsersUserprofileRepository

from nir_myrmiaka.services.auth.security import hash_password, verify_password

from nir_myrmiaka.db.database import Database

from datetime import datetime

from typing import Tuple


class UserService:
    def __init__(self, db: Database):
        self.db = db
        self.auth_user_repo = AuthUserRepository(session=db)
        self.users_userprofile_repo = UsersUserprofileRepository(session=db)

    @staticmethod
    def _extract_from_payload(payload, *args):
        return {key: payload.__getattribute__(key) for key in args}

    async def register_user(self, payload) -> Tuple[AuthUser, UsersUserprofile]:
        existing_user = await self.auth_user_repo.find_one(username=payload.username)
        if existing_user:
            raise ValueError("Username already taken")

        auth_user_data = self._extract_from_payload(
            payload, "password", "username", "first_name", "last_name", "email"
        )

        auth_user_data["password"] = hash_password(auth_user_data["password"])
        auth_user_data["last_login"] = auth_user_data["date_joined"] = datetime.now()

        auth_user = await self.auth_user_repo.create(**auth_user_data)

        users_userprofile_data = self._extract_from_payload(
            payload, "middle_name", "role"
        )
        users_userprofile_data["user_id"] = auth_user.id

        users_userprofile = await self.users_userprofile_repo.create(
            **users_userprofile_data
        )

        return (auth_user, users_userprofile)

    async def login_user(self, username: str, password: str):

        async def authenticate_user(_, username: str, password: str) -> AuthUser | None:
            """Inner logic of authentication."""
            user = await self.auth_user_repo.find_one(username=username)
            if user and verify_password(password, user.password):
                return user
            return None

        user = await authenticate_user(self.db, username, password)

        if not user:
            raise ValueError("Invalid credentials")

        user.last_login = datetime.now()
        return await self.auth_user_repo.save(user)

    async def _extract_existing_userprofile_from_id(
        self, _id: int
    ) -> UsersUserprofile:
        existing_userprofile = await self.users_userprofile_repo.find_one(
            user_id=_id
        )
        if not existing_userprofile:
            raise ValueError("User profile does not found")
        return existing_userprofile

    async def get_status(self, _id: int) -> str:
        existing_userprofile = (
            await self._extract_existing_userprofile_from_id(_id)
        )
        return {"status": existing_userprofile.role}

    async def get_user_info(self, _id: int) -> UsersUserprofile:
        return await self._extract_existing_userprofile_from_id(_id)

    async def get_all_teachers(self) -> tuple[int, list[UsersUserprofile]]:
        return await self.users_userprofile_repo.find_and_count(role="Teacher")

    async def set_user_info(self, payload):
        existing_userprofile = (
            await self._extract_existing_userprofile_from_id(payload.id)
        )
        await self.auth_user_repo.update_by_filter(
            {
                "first_name": payload.first_name,
                "last_name": payload.last_name,
                "email": payload.email,
            },
            id=existing_userprofile.user_id,
        )
        await self.users_userprofile_repo.update_by_filter(
            {"middle_name": payload.middle_name, "group_id": payload.group_id},
            id=existing_userprofile.id,
        )
