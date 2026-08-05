from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Tag
from app.schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


@router.get("/", response_model=list[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    statement = select(Tag)
    result = await db.execute(statement)

    return result.scalars().all()


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Tag).where(Tag.id == tag_id)
    result = await db.execute(statement)
    tag = result.scalar_one_or_none()

    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    return tag


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TagResponse)
async def create_tag(data: TagCreate, db: AsyncSession = Depends(get_db)):
    tag = Tag(
        name=data.name
    )

    db.add(tag)

    await db.commit()
    await db.refresh(tag)

    return tag


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, data: TagUpdate, db: AsyncSession = Depends(get_db)):
    statement = select(Tag).where(Tag.id == tag_id)
    result = await db.execute(statement)
    tag = result.scalar_one_or_none()

    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    if data.name is not None:
        tag.name = data.name

    await db.commit()
    await db.refresh(tag)

    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Tag).where(Tag.id == tag_id)
    result = await db.execute(statement)
    tag = result.scalar_one_or_none()

    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    await db.delete(tag)
    await db.commit()