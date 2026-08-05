from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Folder
from app.schemas.folder import FolderCreate, FolderUpdate, FolderResponse

router = APIRouter(
    prefix="/folders",
    tags=["Folders"]
)


@router.get("/", response_model=list[FolderResponse])
async def get_folders(db: AsyncSession = Depends(get_db)):
    statement = select(Folder)
    result = await db.execute(statement)
    folders = result.scalars().all()

    return folders


@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder(folder_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Folder).where(Folder.id == folder_id)
    result = await db.execute(statement)
    folder = result.scalar_one_or_none()

    if folder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )

    return folder


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=FolderResponse)
async def create_folder(folder_data: FolderCreate, db: AsyncSession = Depends(get_db)):
    folder = Folder(
        name=folder_data.name,
        user_id=folder_data.user_id
    )

    db.add(folder)

    await db.commit()
    await db.refresh(folder)

    return folder


@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder(folder_id: int, updated_data: FolderUpdate, db: AsyncSession = Depends(get_db)):
    statement = select(Folder).where(Folder.id == folder_id)
    result = await db.execute(statement)
    folder = result.scalar_one_or_none()

    if folder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )

    if updated_data.name is not None:
        folder.name = updated_data.name

    await db.commit()
    await db.refresh(folder)

    return folder


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(folder_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Folder).where(Folder.id == folder_id)
    result = await db.execute(statement)
    folder = result.scalar_one_or_none()

    if folder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )

    await db.delete(folder)
    await db.commit()