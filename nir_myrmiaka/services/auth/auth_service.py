from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.models.auth_user import AuthUser
from nir_myrmiaka.db.models.users_userprofile import UsersUserprofile

from nir_myrmiaka.web.api.v1.auth.schemas.requests import UserCreateRequest

from nir_myrmiaka.db.repositories.auth_user import AuthUserRepository
from nir_myrmiaka.db.repositories.users_userprofile import UsersUserprofileRepository

from nir_myrmiaka.services.auth.security import hash_password, verify_password

from datetime import datetime

from typing import Tuple

class UserService:
    def __init__(self, 
                 db: AsyncSession, 
                 auth_user_repo: AuthUserRepository, 
                 users_userpofile_repo: UsersUserprofileRepository):
        self.db = db
        self.auth_user_repo = auth_user_repo
        self.users_userprofile_repo = users_userpofile_repo
    
    async def register_user(self, payload: UserCreateRequest) -> Tuple[AuthUser, UsersUserprofile]:
        existing_user = await self.auth_user_repo.read(self.db, {'username': payload.username})
        if existing_user:
            raise ValueError('Username already taken')
        
        available_auth_user_keys = [
            'password', 'username', 'first_name',
            'last_name', 'email', 'is_superuser',
            'is_staff', 'is_active'
        ]
        
        auth_user_data = {
            key: payload.__getattribute__(key) for key in available_auth_user_keys
        }
        
        auth_user_data['password'] = hash_password(auth_user_data['password'])
        auth_user_data['last_login'] = auth_user_data['date_joined'] = datetime.now()
        
        auth_user = await self.auth_user_repo.create(self.db, auth_user_data)
        
        available_users_userprofile_keys = [
            'middle_name', 'role'
        ]
        
        users_userprofile_data = {
            key: payload.__getattribute__(key) for key in available_users_userprofile_keys
        }
        
        users_userprofile_data['user_id'] = auth_user.id
        
        users_userprofile = await self.users_userprofile_repo.create(self.db, users_userprofile_data)
        
        return (auth_user, users_userprofile)
    
    async def login_user(self, username: str, password: str):
        async def authenticate_user(db, username: str, password: str):
            """Inner logic of authentication."""
            user = await self.auth_user_repo.read(db, {'username': username})
            if user and verify_password(password, user.password):
                return user
            return None
        
        user = await authenticate_user(self.db, username, password)
        
        if not user:
            raise ValueError("Invalid credentials")
        
        user.last_login = datetime.now()
        await self.db.commit()
        
    async def _extract_existing_data_from_username(self, username: str) -> Tuple[AuthUser, UsersUserprofile]:
        existing_auth_user = await self.auth_user_repo.read(self.db, {'username': username})
        if not existing_auth_user:
            raise ValueError('User with that username does not exist')
        existing_userprofile = await self.users_userprofile_repo.read(self.db, {'user_id': existing_auth_user.id})
        if not existing_userprofile:
            raise ValueError('User profile does not found')
        return (existing_auth_user, existing_userprofile)
    
    async def get_status(self, username: str) -> str:
        _, existing_userprofile = await self._extract_existing_data_from_username(username)
        return {'status': existing_userprofile.role}
        
    async def get_user_info(self, username: str) -> str:
        existing_auth_user, existing_userprofile = await self._extract_existing_data_from_username(username)
        return {
            'username': username, 
            'email': existing_auth_user.email, 
            'first_name': existing_auth_user.first_name, 
            'last_name': existing_auth_user.last_name, 
            'middle_name': existing_userprofile.middle_name,
            'group': existing_userprofile.group_id
        }