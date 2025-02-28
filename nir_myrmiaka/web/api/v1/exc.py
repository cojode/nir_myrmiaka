from fastapi import HTTPException, status


def raise_http_error_from_exception(
    e: Exception,
    provide_detail: bool = True,
    custom_status: status = status.HTTP_400_BAD_REQUEST,
):
    raise HTTPException(
        status_code=custom_status,
        detail=str(e) if provide_detail else None,
    ) from e
