from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.tag import TagRepository
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.services.tag import TagService

router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


def get_tag_service(db: AsyncSession = Depends(get_db)) -> TagService:
    repository = TagRepository(db)
    return TagService(repository)


@router.get("/", response_model=list[TagResponse])
async def get_tags(service: TagService = Depends(get_tag_service)):
    return await service.get_all_tags()


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: int,
    service: TagService = Depends(get_tag_service)
):
    return await service.get_tag_by_id(tag_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TagResponse
)
async def create_tag(
    tag_data: TagCreate,
    service: TagService = Depends(get_tag_service)
):
    return await service.create_tag(tag_data)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    service: TagService = Depends(get_tag_service)
):
    return await service.update_tag(tag_id, tag_data)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    service: TagService = Depends(get_tag_service)
):
    await service.delete_tag(tag_id)