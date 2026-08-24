from app.core.exceptions import NoteNotFoundException, FolderNotFoundException
from app.models import Note
from app.repositories.note import NoteRepository
from app.repositories.folder import FolderRepository
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.schemas.pagination import PaginatedResponse


class NoteService:
    def __init__(self, repository: NoteRepository, folder_repository: FolderRepository):
        self.repository = repository
        self.folder_repository = folder_repository
    
    async def get_all_notes(
            self,
            page: int = 1,
            limit: int = 10,
            q: str | None = None,
            sort_by: str = "created_at",
            order: str = "asc",
            folder_id: int | None = None,
            user_id: int | None = None,
    ) -> PaginatedResponse[NoteResponse]:
        offset = (page - 1) * limit

        if folder_id is None and user_id is None:
            raise ValueError("Must provide either folder_id or user_id as a query parameter.") 
        
        items, total = await self.repository.get_all(
            offset=offset,
            limit=limit,
            q=q,
            sort_by=sort_by,
            order=order,
            folder_id=folder_id,
            user_id=user_id
            )

        return PaginatedResponse[NoteResponse](
            items=items,
            total=total,
            page=page,
            limit=limit
        )

    async def get_note_by_id(self, note_id: int) -> Note:
        note = await self.repository.get_by_id(note_id)
        if note is None:
            raise NoteNotFoundException(f"Note with ID {note_id} not found")
        return note

    async def validate_folder(
    self,
    user_id: int,
    folder_id: int | None,
) -> None:

        if folder_id is None:
            return
    
        folder = await self.folder_repository.get_by_id(folder_id)
    
        if folder is None:
            raise FolderNotFoundException(
                f"Folder with ID {folder_id} not found"
            )
    
        if folder.user_id != user_id:
            raise FolderNotFoundException(
                f"Folder with ID {folder_id} not found"
            )
    
        
    async def create_note(
    self,
    note_data: NoteCreate,
) -> Note:

        await self.validate_folder(
            user_id=note_data.user_id,
            folder_id=note_data.folder_id,
        )
    
        note = Note(
            user_id=note_data.user_id,
            folder_id=note_data.folder_id,
            title=note_data.title,
            content=note_data.content,
        )

        return await self.repository.create(note)


    async def update_note(
    self,
    note_id: int,
    note_data: NoteUpdate,
) -> Note:

        note = await self.get_note_by_id(note_id)
    
        if "folder_id" in note_data.model_fields_set:
            await self.validate_folder(
                user_id=note.user_id,
                folder_id=note_data.folder_id,
            )
    
            note.folder_id = note_data.folder_id
    
        if "title" in note_data.model_fields_set:
            note.title = note_data.title
        
        if "content" in note_data.model_fields_set:
            note.content = note_data.content
            
        return await self.repository.update(note)
    
    async def delete_note(self, note_id: int) -> None:
        note = await self.get_note_by_id(note_id)
        await self.repository.delete(note)