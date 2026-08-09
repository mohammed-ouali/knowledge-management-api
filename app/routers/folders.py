from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.folder import FolderRepository
from app.schemas.folder import FolderCreate, FolderResponse, FolderUpdate
from app.services.folder import FolderService

router = APIRouter(
    prefix="/folders", 
    tags=["Folders"]
)


def get_folder_service(db: AsyncSession = Depends(get_db)) -> FolderService:
    repository = FolderRepository(db)
    return FolderService(repository)


@router.get("/", response_model=list[FolderResponse])  
async def get_folders_by_user(
    user_id: int,
    service: FolderService = Depends(get_folder_service)
):
    return await service.get_all_folders(user_id)


@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder(
    folder_id: int,
    service: FolderService = Depends(get_folder_service)
):
    return await service.get_folder_by_id(folder_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=FolderResponse
)
async def create_folder(
    folder_data: FolderCreate,
    service: FolderService = Depends(get_folder_service)
):
    return await service.create_folder(folder_data)


@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: int,
    folder_data: FolderUpdate,
    service: FolderService = Depends(get_folder_service)
):
    return await service.update_folder(folder_id, folder_data)


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(
    folder_id: int,
    service: FolderService = Depends(get_folder_service)
):
    await service.delete_folder(folder_id)