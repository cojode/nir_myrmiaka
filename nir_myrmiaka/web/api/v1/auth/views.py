from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.dependencies import get_db_session
from nir_myrmiaka.db.repositories.auth import (
    authenticate_user
)
from nir_myrmiaka.db.repositories.users import (
    get_user_by_username, create_user
)
from nir_myrmiaka.web.api.v1.auth.schemas.requests import (
    UserCreateRequest
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        user_in: UserCreateRequest,
        db: AsyncSession = Depends(get_db_session)
    ):
    """
    Checks if provided user create request contains unqiue login
    Register new user with 201
    Unless returns 400
    """
    existing_user_login = await get_user_by_username(db, user_in.username)
    if existing_user_login:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already taken')
    return await create_user(db, user_in)

@router.post("/login", summary="Authenticates a user", status_code=status.HTTP_200_OK)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
    )
    return {}