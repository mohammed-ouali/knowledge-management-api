from fastapi import APIRouter
from fastapi import HTTPException, status
from app.schemas.note import CreateNote, NoteResponse, UpdateNote

router = APIRouter(prefix= "/notes", tags= ["Notes"])

notes = []


@router.get("/", response_model= list[NoteResponse])
async def get_notes():
    return notes


@router.get("/{id}", response_model= NoteResponse)
async def get_note(id: int):
    for note in notes:
        if note["id"] == id:
            return note
    raise HTTPException(
        status_code=404,
        detail="Note not found")


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= NoteResponse)
async def create_note(note: CreateNote):
    note = note.model_dump()
    note["id"] = len(notes) + 1
    notes.append(note)
    return note


@router.put("/{id}", response_model= NoteResponse)
async def update_note(id: int, updated_note: UpdateNote):
    for note in notes:
        if note["id"] == id:
            note["title"] = updated_note.title
            note["content"] = updated_note.content
            return note
    raise HTTPException(
        status_code=404,
        detail="Note not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id: int):
    for note in notes:
        if note["id"] == id:
            notes.remove(note)
            return
    raise HTTPException(
        status_code=404,
        detail="Note not found")