from fastapi import APIRouter

from app.api.v1.routers import (
    users,
    folders,
    notes,
    auth
)

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(folders.router)
api_router.include_router(notes.router)
api_router.include_router(notes.auth)