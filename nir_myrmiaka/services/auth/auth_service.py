from nir_myrmiaka.db.models.user_profile import UserProfile

from nir_myrmiaka.db.repositories.user_profile import UserProfileRepository

from nir_myrmiaka.services.auth.security import hash_password, verify_password

from nir_myrmiaka.db.database import Database

from datetime import datetime


class UserService:
    def __init__(self, db: Database):
        self.db = db
        self.user_profile_repo = UserProfileRepository(session=db)

    @staticmethod
    def _extract_from_payload(payload, *args):
        return {key: payload.__getattribute__(key) for key in args}

    async def register_user(self, data: dict[str, any]) -> UserProfile:
        existing_user = await self.user_profile_repo.find_one(
            username=data["username"]
        )
        if existing_user:
            raise ValueError("Username already taken")

        data["password"] = hash_password(data["password"])
        data["last_login"] = data["date_joined"] = datetime.now()

        new_user = await self.user_profile_repo.create(**data)

        return new_user

    async def login_user(self, username: str, password: str):

        async def authenticate_user(
            _, username: str, password: str
        ) -> UserProfile | None:
            """Inner logic of authentication."""
            user = await self.user_profile_repo.find_one(username=username)
            if user and verify_password(password, user.password):
                return user
            return None

        user = await authenticate_user(self.db, username, password)

        if not user:
            raise ValueError("Invalid credentials")

        user.last_login = datetime.now()
        return await self.user_profile_repo.save(user)

    async def _extract_existing_userprofile_from_id(
        self, _id: int
    ) -> UserProfile:
        existing_userprofile = await self.user_profile_repo.find_one(id=_id)
        if not existing_userprofile:
            raise ValueError("User does not exists")
        return existing_userprofile

    async def get_status(self, _id: int) -> str:
        existing_userprofile = (
            await self._extract_existing_userprofile_from_id(_id)
        )
        return {"status": existing_userprofile.role}

    async def get_user_info(self, _id: int) -> UserProfile:
        return await self._extract_existing_userprofile_from_id(_id)

    async def get_all_teachers(self) -> tuple[int, list[UserProfile]]:
        return await self.user_profile_repo.find_and_count(role="Teacher")

    async def set_user_info(
        self,
        payload: dict[str, any],
    ):
        target_id = payload["target"]["user_id"]
        await self._extract_existing_userprofile_from_id(target_id)
        await self.user_profile_repo.update_by_filter(
            fields=payload["data"], id=target_id
        )

    async def verify_exists_and_role_specified(self, user_id, role: str):
        user: UserProfile = await self.user_profile_repo.find_one(id=user_id)
        if user == None:
            raise ValueError(
                f"User with provided id {user_id} does not exists"
            )
        if user.role != role:
            raise ValueError(
                f"User with provided id {user_id} does not have specified role ({role})"
            )
