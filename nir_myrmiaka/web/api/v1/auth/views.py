from fastapi import APIRouter, HTTPException, Depends, status, Request

from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.dependencies import get_db_session
from nir_myrmiaka.db.repositories.users import (
    get_user_by_login, get_user_by_id, create_user
)
from nir_myrmiaka.web.api.v1.auth.schemas.requests import (
    UserCreateRequest
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        user_in: UserCreateRequest,
        db: AsyncSession = Depends(get_db_session)
    ) -> None:
    """
    Checks if provided user create request contains unqiue login
    Register new user with 201
    Unless returns 400
    """
    existing_user_login = await get_user_by_login(db, user_in.login)
    if existing_user_login:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Login already taken')
    user = await create_user(db, user_in)
    return user
