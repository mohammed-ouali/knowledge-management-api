from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Note
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.get("/", response_model=list[NoteResponse])
async def get_notes(db: AsyncSession = Depends(get_db)):
    statement = select(Note)
    result = await db.execute(statement)
    notes = result.scalars().all()

    return notes


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Note).where(Note.id == note_id)
    result = await db.execute(statement)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return note


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteResponse
)
async def create_note(
    note_data: NoteCreate,
    db: AsyncSession = Depends(get_db)
):
    note = Note(
        title=note_data.title,
        content=note_data.content,
        folder_id=note_data.folder_id,
        author_id=note_data.author_id
    )

    db.add(note)

    await db.commit()
    await db.refresh(note)

    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    updated_data: NoteUpdate,
    db: AsyncSession = Depends(get_db)
):
    statement = select(Note).where(Note.id == note_id)
    result = await db.execute(statement)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    if updated_data.title is not None:
        note.title = updated_data.title

    if updated_data.content is not None:
        note.content = updated_data.content

    if updated_data.folder_id is not None:
        note.folder_id = updated_data.folder_id

    note.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(note)

    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db)
):
    statement = select(Note).where(Note.id == note_id)
    result = await db.execute(statement)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    await db.delete(note)

    await db.commit()