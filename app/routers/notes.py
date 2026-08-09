from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.note import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.services.note import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


def get_note_service(db: AsyncSession = Depends(get_db)) -> NoteService:
    repository = NoteRepository(db)
    return NoteService(repository)


@router.get("/", response_model=list[NoteResponse])
async def get_notes(
    folder_id: int | None = None,
    author_id: int | None = None,
    service: NoteService = Depends(get_note_service)
):
    if folder_id is not None:
        return await service.get_all_notes_by_folder(folder_id)
    if author_id is not None:
        return await service.get_all_notes_by_author(author_id)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Must provide either folder_id or author_id as a query parameter"
    )


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    service: NoteService = Depends(get_note_service)
):
    return await service.get_note_by_id(note_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteResponse
)
async def create_note(
    note_data: NoteCreate,
    service: NoteService = Depends(get_note_service)
):
    return await service.create_note(note_data)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    service: NoteService = Depends(get_note_service)
):
    return await service.update_note(note_id, note_data)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    service: NoteService = Depends(get_note_service)
):
    await service.delete_note(note_id)