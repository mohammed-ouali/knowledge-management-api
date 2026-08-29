from fastapi import FastAPI

from app.core.config import settings

from app.api.v1.router import api_router

from app.middlewares.performance import PerformanceMiddleware

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug
)


@app.get("/")
async def root():
    return {"message": "API is running"}

app.add_middleware(
    PerformanceMiddleware,
)

app.include_router(api_router, prefix="/api/v1")

