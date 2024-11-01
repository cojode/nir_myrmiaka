from fastapi.routing import APIRouter

from backend.web.api.v1 import monitoring

from backend.settings import settings

api_router = APIRouter()

api_router.include_router(monitoring.router)
# api_router.include_router(docs.router, prefix=f"/{settings.api_version}")
