from app.core.exceptions import TagAlreadyExistsException, TagNotFoundException
from app.models import Tag
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagCreate, TagUpdate


class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository

    async def get_all_tags(self) -> list[Tag]:
        return await self.repository.get_all()

    async def get_tag_by_id(self, tag_id: int) -> Tag:
        tag = await self.repository.get_by_id(tag_id)
        if tag is None:
            raise TagNotFoundException(f"Tag with ID {tag_id} not found")
        return tag

    async def create_tag(self, tag_data: TagCreate) -> Tag:
        existing_tag = await self.repository.get_by_name(tag_data.name)
        if existing_tag is not None:
            raise TagAlreadyExistsException(f"Tag '{tag_data.name}' already exists")

        tag = Tag(name=tag_data.name)
        return await self.repository.create(tag)

    async def update_tag(self, tag_id: int, tag_data: TagUpdate) -> Tag:
        tag = await self.get_tag_by_id(tag_id)

        if tag_data.name is not None and tag_data.name != tag.name:
            existing_tag = await self.repository.get_by_name(tag_data.name)
            if existing_tag is not None:
                raise TagAlreadyExistsException(f"Tag '{tag_data.name}' already exists")
            tag.name = tag_data.name

        return await self.repository.update(tag)

    async def delete_tag(self, tag_id: int) -> None:
        tag = await self.get_tag_by_id(tag_id)
        await self.repository.delete(tag)