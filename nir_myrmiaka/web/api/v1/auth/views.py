from fastapi import APIRouter, HTTPException, Depends, status, Request

from sqlalchemy.ext.asyncio import AsyncSession

from nir_myrmiaka.db.dependencies import get_db_session
from nir_myrmiaka.web.api.v1.auth.schemas.requests import (
    UserCreateRequest
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user( 
        request: Request,
        user_in: UserCreateRequest,
        db: AsyncSession = Depends(get_db_session)
    ) -> None:
    """
    Register new user
    """
    return user_in
