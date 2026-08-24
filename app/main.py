from fastapi import FastAPI

from app.core.config import settings

from app.api.v1.router import api_router

from app.middlewares.logging import PerformanceLoggingMiddleware

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug
)


@app.get("/")
async def root():
    return {"message": "API is running"}


app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    PerformanceLoggingMiddleware
)