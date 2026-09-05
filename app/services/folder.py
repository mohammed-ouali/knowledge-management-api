from app.core.exceptions import (
    InvalidFolderHierarchyException,
    FolderAlreadyExistsException,
    FolderNotFoundException,
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
        page: int = 1,
        limit: int = 10,
        q: str | None = None,
        sort_by: str = "created_at",
        order: str = "asc",
        user_id: int | None = None,
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
    ) -> Folder:

        folder = await self.repository.get_by_id(folder_id)

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

        parent = await self.repository.get_by_id(parent_id)

        if parent is None:
            raise FolderNotFoundException(
                f"Parent folder with ID {parent_id} not found"
            )

        if parent.user_id != user_id:
            raise FolderNotFoundException(
                f"Parent folder with ID {parent_id} not found"
            )

        if current_folder_id is not None:
            if parent_id == current_folder_id:
                raise InvalidFolderHierarchyException(
                    "Folder cannot be its own parent"
                )

        visited: set[int] = set()
        current = parent
        
        while current is not None:
        
            if current.id in visited:
                raise InvalidFolderHierarchyException(
                    "Circular folder hierarchy detected"
                )
        
            visited.add(current.id)
        
            if current.id == current_folder_id:
                raise InvalidFolderHierarchyException(
                    "Folder cannot become a descendant of itself"
                )
        
            if current.parent_id is None:
                break
        
            current = await self.repository.get_by_id(
                current.parent_id
            )

    async def get_children(
        self,
        folder_id: int,
    ) -> list[Folder]:

        folder = await self.get_folder_by_id(folder_id)

        return await self.repository.get_children(
            parent_id=folder.id,
            user_id=folder.user_id,
        )

    async def get_folder_notes(
        self,
        folder_id: int,
        page: int = 1,
        limit: int = 10,
    ) -> PaginatedResponse[NoteResponse]:

        folder = await self.get_folder_by_id(folder_id)

        offset = (page - 1) * limit

        notes, total = await self.repository.get_notes(
            folder_id=folder.id,
            user_id=folder.user_id,
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
    ) -> Folder:

        existing_folder = (
            await self.repository.get_by_name_and_parent(
                user_id=folder_data.user_id,
                name=folder_data.name,
                parent_id=folder_data.parent_id,
            )
        )

        if existing_folder:
            raise FolderAlreadyExistsException(
                f"Folder with the name "
                f"{folder_data.name} already exists "
                f"in this folder"
            )

        await self.validate_parent(
            user_id=folder_data.user_id,
            parent_id=folder_data.parent_id,
        )

        folder = Folder(
            name=folder_data.name,
            user_id=folder_data.user_id,
            parent_id=folder_data.parent_id,
        )

        return await self.repository.create(folder)

    async def update_folder(
        self,
        folder_id: int,
        folder_data: FolderUpdate,
    ) -> Folder:

        folder = await self.get_folder_by_id(folder_id)

        new_name = (
            folder_data.name
            if folder_data.name is not None
            else folder.name
        )

        new_parent_id = (
            folder_data.parent_id
            if folder_data.parent_id is not None
            else folder.parent_id
        )

        if (
            new_name != folder.name
            or new_parent_id != folder.parent_id
        ):
            existing_folder = (
                await self.repository.get_by_name_and_parent(
                    user_id=folder.user_id,
                    name=new_name,
                    parent_id=new_parent_id,
                )
            )

            if (
                existing_folder
                and existing_folder.id != folder.id
            ):
                raise FolderAlreadyExistsException(
                    f"Folder with the name "
                    f"{new_name} already exists "
                    f"in this folder"
                )

        if folder_data.parent_id is not None:
            await self.validate_parent(
                user_id=folder.user_id,
                parent_id=folder_data.parent_id,
                current_folder_id=folder.id,
            )

        if folder_data.name is not None:
            folder.name = folder_data.name

        if folder_data.parent_id is not None:
            folder.parent_id = folder_data.parent_id

        return await self.repository.update(folder)

    async def delete_folder(
        self,
        folder_id: int,
    ) -> None:

        folder = await self.get_folder_by_id(folder_id)

        await self.repository.delete(folder)