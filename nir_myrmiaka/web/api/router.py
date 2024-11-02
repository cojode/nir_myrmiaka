from fastapi.routing import APIRouter

from nir_myrmiaka.web.api.v1 import monitoring, auth, user

from nir_myrmiaka.settings import settings

api_router = APIRouter()

api_router.include_router(monitoring.router)
api_router.include_router(auth.router, prefix=f"/{settings.api_version}")
api_router.include_router(user.router, prefix=f"/{settings.api_version}")