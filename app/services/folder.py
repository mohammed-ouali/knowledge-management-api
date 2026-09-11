from app.core.exceptions import (
    FolderAlreadyExistsException,
    FolderNotFoundException,
    InvalidFolderHierarchyException,
)
from app.models import Folder
from app.repositories.folder import FolderRepository
from app.schemas.folder import (
    FolderCreate,
    FolderResponse,
    FolderUpdate,
)
from app.schemas.note import NoteResponse
from app.schemas.pagination import PaginatedResponse


class FolderService:

    def __init__(
        self,
        repository: FolderRepository,
    ):
        self.repository = repository

    async def get_all_folders(
        self,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        q: str | None = None,
        sort_by: str = "created_at",
        order: str = "asc",
    ) -> PaginatedResponse[FolderResponse]:

        offset = (page - 1) * limit

        folders, total = await self.repository.get_all(
            offset=offset,
            limit=limit,
            q=q,
            sort_by=sort_by,
            order=order,
            user_id=user_id,
        )

        return PaginatedResponse[FolderResponse](
            items=folders,
            total=total,
            page=page,
            limit=limit,
        )

    async def get_folder_by_id(
        self,
        folder_id: int,
        user_id: int,
    ) -> Folder:

        folder = await self.repository.get_by_id(folder_id=folder_id, user_id=user_id)

        if folder is None:
            raise FolderNotFoundException(
                f"Folder with ID {folder_id} not found"
            )

        return folder

    async def validate_parent(
        self,
        user_id: int,
        parent_id: int | None,
        current_folder_id: int | None = None,
    ) -> None:
        if parent_id is None:
            return
    
        parent = await self.get_folder_by_id(folder_id=parent_id, user_id=user_id)
    
        if current_folder_id is not None and parent_id == current_folder_id:
            raise InvalidFolderHierarchyException("Folder cannot be its own parent")
    
        current = parent
        while current.parent_id is not None:
            if current.parent_id == current_folder_id:
                raise InvalidFolderHierarchyException(
                    "Folder cannot become a descendant of itself"
                )
    
            current = await self.get_folder_by_id(
                folder_id=current.parent_id, user_id=user_id
            )

    async def get_children(
        self,
        folder_id: int,
        user_id: int,
    ) -> list[Folder]:

        folder = await self.get_folder_by_id(folder_id=folder_id, user_id=user_id)

        return await self.repository.get_children(
            parent_id=folder.id,
            user_id=user_id,
        )

    async def get_folder_notes(
        self,
        folder_id: int,
        user_id: int,
        page: int = 1,
        limit: int = 10,
    ) -> PaginatedResponse[NoteResponse]:

        folder = await self.get_folder_by_id(folder_id=folder_id, user_id=user_id)

        offset = (page - 1) * limit

        notes, total = await self.repository.get_notes(
            folder_id=folder.id,
            user_id=user_id,
            offset=offset,
            limit=limit,
        )

        return PaginatedResponse[NoteResponse](
            items=notes,
            total=total,
            page=page,
            limit=limit,
        )

    async def create_folder(
        self,
        folder_data: FolderCreate,
        user_id: int,
    ) -> Folder:

        existing_folder = await self.repository.get_by_name_and_parent(
            user_id=user_id,
            name=folder_data.name,
            parent_id=folder_data.parent_id,
        )

        if existing_folder:
            raise FolderAlreadyExistsException(
                f"Folder with the name '{folder_data.name}' already exists in this directory"
            )

        await self.validate_parent(
            user_id=user_id,
            parent_id=folder_data.parent_id,
        )

        folder = Folder(
            name=folder_data.name,
            user_id=user_id,
            parent_id=folder_data.parent_id,
        )

        return await self.repository.create(folder=folder)

    async def update_folder(
        self,
        folder_id: int,
        folder_data: FolderUpdate,
        user_id: int,
    ) -> Folder:
    
        folder = await self.get_folder_by_id(folder_id=folder_id, user_id=user_id)
    
        update_data = folder_data.model_dump(exclude_unset=True)
    
        new_name = update_data.get("name", folder.name)
        new_parent_id = update_data.get("parent_id", folder.parent_id)
    
        if new_name != folder.name or new_parent_id != folder.parent_id:
            existing_folder = await self.repository.get_by_name_and_parent(
                user_id=user_id,
                name=new_name,
                parent_id=new_parent_id,
            )
    
            if existing_folder and existing_folder.id != folder.id:
                raise FolderAlreadyExistsException(
                    f"Folder with the name '{new_name}' already exists in this directory"
                )
    
        if "parent_id" in update_data and update_data["parent_id"] != folder.parent_id:
            await self.validate_parent(
                user_id=user_id,
                parent_id=new_parent_id,
                current_folder_id=folder.id,
            )
    
        if "name" in update_data:
            folder.name = update_data["name"]
    
        if "parent_id" in update_data:
            folder.parent_id = update_data["parent_id"]
    
        return await self.repository.update(folder=folder)

    async def delete_folder(
        self,
        folder_id: int,
        user_id: int,
    ) -> None:

        folder = await self.get_folder_by_id(folder_id=folder_id, user_id=user_id)

        await self.repository.delete(folder=folder)