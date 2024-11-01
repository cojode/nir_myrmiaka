from fastapi.routing import APIRouter

from nir_myrmiaka.web.api.v1 import monitoring

from nir_myrmiaka.settings import settings

api_router = APIRouter()

api_router.include_router(monitoring.router)
# api_router.include_router(docs.router, prefix=f"/{settings.api_version}")
