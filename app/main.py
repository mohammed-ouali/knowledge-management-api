from fastapi import FastAPI

from app.routers.notes import router as notes_router
from app.routers.users import router as users_router
from app.config import settings

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