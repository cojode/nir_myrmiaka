from nir_myrmiaka.exceptions.abc import BaseError, DomainError, RepositoryError
from pydantic import ValidationError
from fastapi import Request
from fastapi.responses import JSONResponse

from nir_myrmiaka.web.api.v1.schemas import ApplicationErrorResponse

from collections.abc import Callable

from typing import Any

from nir_myrmiaka.log import logger


async def application_exception_middleware(
    request: Request, call_next: Callable[[Request], Any]
) -> JSONResponse:
    """
    Middleware to handle exceptions in the application.

    This function wraps the request processing and catches any exceptions
    that occur. It returns a JSON response with the error message and status code.

    :param request: The request object.
    :param call_next: The next middleware or route handler.
    :return: A JSON response with the error message and status code.
    """
    try:
        return await call_next(request)
    except BaseError as exc:
        return await application_exception_handler(request, exc)
    except ValidationError as exc:
        logger.error("Validation error: %s", exc.errors())
        raise exc
    except Exception as exc:
        logger.error("Unexpected error: %s", exc)
        raise exc


async def application_exception_handler(
    _: Request, exc: BaseError
) -> JSONResponse:
    """
    Custom exception handler for the application.

    This function handles exceptions raised during the processing of a request.
    It returns a JSON response with the error message and status code.

    :param request: The request object.
    :param exc: The exception object.
    :return: A JSON response with the error message and status code.
    """
    status_code_map = {RepositoryError: 500, DomainError: 400}

    for error_type, status_code in status_code_map.items():
        if isinstance(exc, error_type):
            return JSONResponse(
                content=ApplicationErrorResponse(
                    error=exc.error,
                    msg=exc.message,
                    detail=exc.detail,
                ).model_dump(),
                status_code=status_code,
            )
