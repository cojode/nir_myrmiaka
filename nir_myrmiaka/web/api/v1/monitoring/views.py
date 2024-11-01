from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health/", status_code=status.HTTP_200_OK)
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return {}
