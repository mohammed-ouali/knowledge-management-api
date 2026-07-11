from fastapi import FastAPI

from app.routers.notes import router as notes_router
from app.routers.users import router as users_router
from app.routers.folders import router as folders_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API is running"}


app.include_router(notes_router)
app.include_router(users_router)
app.include_router(folders_router)