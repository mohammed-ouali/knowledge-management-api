from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.exceptions import DomainException
from app.core.config import settings
from app.api.v1.router import api_router
from app.middlewares.performance import PerformanceMiddleware
from app.core.exception_handlers import (
    domain_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug
)


@app.get("/")
async def root():
    return {"message": "API is running"}

app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(PerformanceMiddleware)

app.include_router(api_router, prefix="/api/v1")

