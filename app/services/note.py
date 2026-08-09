from datetime import datetime, timezone

from app.core.exceptions import NoteNotFoundException
from app.models import Note
from app.repositories.note import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, repository: NoteRepository):
        self.repository = repository

    async def get_all_notes_by_folder(self, folder_id: int) -> list[Note]:
        return await self.repository.get_all_by_folder(folder_id)

    async def get_all_notes_by_author(self, author_id: int) -> list[Note]:
        return await self.repository.get_all_by_author(author_id)

    async def get_note_by_id(self, note_id: int) -> Note:
        note = await self.repository.get_by_id(note_id)
        if note is None:
            raise NoteNotFoundException(f"Note with ID {note_id} not found")
        return note

    async def create_note(self, note_data: NoteCreate) -> Note:
        note = Note(
            folder_id=note_data.folder_id,
            author_id=note_data.author_id,
            title=note_data.title,
            content=note_data.content,
        )
        return await self.repository.create(note)

    async def update_note(self, note_id: int, note_data: NoteUpdate) -> Note:
        note = await self.get_note_by_id(note_id)

        if note_data.folder_id is not None:
            note.folder_id = note_data.folder_id

        if note_data.title is not None:
            note.title = note_data.title

        if note_data.content is not None:
            note.content = note_data.content

        note.updated_at = datetime.now(timezone.utc)

        return await self.repository.update(note)

    async def delete_note(self, note_id: int) -> None:
        note = await self.get_note_by_id(note_id)
        await self.repository.delete(note)