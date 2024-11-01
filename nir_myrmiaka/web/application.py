from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from nir_myrmiaka.web.api.router import api_router
from nir_myrmiaka.web.lifespan import lifespan_setup

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="nir_myrmiaka",
        version=metadata.version("nir_myrmiaka"),
        lifespan=lifespan_setup,
        docs_url="/api/docs/",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    
    app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")

    return app
