from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from nir_myrmiaka.log import configure_logging
from nir_myrmiaka.web.api.router import api_router
from nir_myrmiaka.web.lifespan import lifespan_setup

from nir_myrmiaka.web.middleware import application_exception_middleware


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="nir_myrmiaka",
        version=metadata.version("nir_myrmiaka"),
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    app.middleware("http")(application_exception_middleware)

    return app
