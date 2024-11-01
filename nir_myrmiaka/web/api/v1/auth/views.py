from fastapi import APIRouter, HTTPException, Depends, status, Request

router = APIRouter()


@router.get("/register", status_code=status.HTTP_201_CREATED)
async def register_user() -> None:
    """
    Register new user
    """
    return {}
