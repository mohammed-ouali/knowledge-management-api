from app.models import Folder
from app.schemas.folder import FolderCreate, FolderUpdate
from app.repositories.folder import FolderRepository
from app.core.exceptions import FolderAlreadyExistsException, FolderNotFoundException

class FolderService:
    def __init__(self, repository: FolderRepository):
        self.repository = repository

    async def get_all_folders(self, user_id: int) -> list[Folder]:
        return await self.repository.get_all_by_user(user_id)
        

    async def get_folder_by_id(self, folder_id: int) -> Folder:
        folder = await self.repository.get_by_id(folder_id)
        if folder is None:
            raise FolderNotFoundException(f"Folder with ID {folder_id} not found")
        return folder

    async def create_folder(self, folder_data: FolderCreate) -> Folder :
        if await self.repository.get_by_name_and_user(folder_data.user_id, folder_data.name):
            raise FolderAlreadyExistsException(f"Folder with the name {folder_data.name} already exists")

        folder = Folder(
            name = folder_data.name,
            user_id = folder_data.user_id
        )

        return await self.repository.create(folder)

    async def update_folder(self, folder_id: int, folder_data: FolderUpdate) -> Folder:
        folder = await self.get_folder_by_id(folder_id)
        if folder_data.name is not None and folder_data.name != folder.name:
            existing_folder = await self.repository.get_by_name_and_user(folder.user_id, folder_data.name)
            if existing_folder:
                raise FolderAlreadyExistsException(f"Folder with the name {folder_data.name} already exists")
        folder.name = folder_data.name
        return await self.repository.update(folder)

    async def delete_folder(self, folder_id: int) -> None:
        folder = await self.get_folder_by_id(folder_id)
        await self.repository.delete(folder)
        