from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.dependencies import get_db_session
from nir_myrmiaka.db.repositories.auth import (
    authenticate_user, create_user
)
from nir_myrmiaka.db.repositories.users import (
    get_user_by_username
)

from nir_myrmiaka.db.repositories.status import (
    get_status_id
)

from nir_myrmiaka.db.repositories.student import (
    create_student
)

from nir_myrmiaka.db.repositories.teacher import (
    create_teacher
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
    existing_username = await get_user_by_username(db, user_in.username)
    correct_status_id = await get_status_id(db, user_in.status)
    if existing_username or not correct_status_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already taken')
    
    created_user = await create_user(db, user_in, correct_status_id)
    
    status_entity = None
    
    match user_in.status:
        case "student":
            status_entity = await create_student(db, created_user.user_id)
        case "teacher":
            status_entity = await create_teacher(db, created_user.user_id)
        case _:
            pass
    return {"created_user": created_user, f"created_{user_in.status}": status_entity}

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