from fastapi import status
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ProblemDetails,
    DomainException,
    DOMAIN_EXCEPTION_MAP
)


async def domain_exception_handler(
        request: Request, exception: DomainException
) -> JSONResponse:
    status_code, title = DOMAIN_EXCEPTION_MAP.get(
        tuple(exception), (status.HTTP_400_BAD_REQUEST, "Bad request")
        )

    problem = ProblemDetails(
        type="about:blank",
        title=title,
        status=status_code,
        detail=exception.message,
        instance=request.url.path
    )

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(problem),
        media_type="application/problem+json",
    )
