from fastapi.routing import APIRouter

from nir_myrmiaka.web.api.v1 import (
    monitoring,
    auth,
    user,
    student,
    teacher,
    assignment,
    submission,
    notification,
)

from nir_myrmiaka.settings import settings

api_router = APIRouter()

api_router.include_router(monitoring.router)
api_router.include_router(auth.router, prefix=f"/{settings.version}/auth")
api_router.include_router(user.router, prefix=f"/{settings.version}/user")
api_router.include_router(student.router, prefix=f"/{settings.version}/student")
api_router.include_router(teacher.router, prefix=f"/{settings.version}/teacher")
api_router.include_router(
    assignment.router, prefix=f"/{settings.version}/assignment"
)
api_router.include_router(
    submission.router, prefix=f"/{settings.version}/submission"
)
api_router.include_router(
    notification.router, prefix=f"/{settings.version}/notification"
)
