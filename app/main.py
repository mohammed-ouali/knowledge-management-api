from fastapi import FastAPI

from app.core.config import settings

from app.routers.notes import router as notes_router
from app.routers.users import router as users_router
from app.routers.folders import router as folders_router
from app.routers.comments import router as comments_router
from app.routers.tags import router as tags_router

from app.middlewares.logging import PerformanceLoggingMiddleware

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug
)


@app.get("/")
async def root():
    return {"message": "API is running"}


app.include_router(notes_router)
app.include_router(users_router)
app.include_router(folders_router)
app.include_router(comments_router)
app.include_router(tags_router)

app.add_middleware(
    PerformanceLoggingMiddleware
)