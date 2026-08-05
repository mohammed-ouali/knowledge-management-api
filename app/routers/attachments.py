from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Attachment
from app.schemas.attachment import AttachmentCreate, AttachmentUpdate, AttachmentResponse

router = APIRouter(
    prefix="/attachments",
    tags=["Attachments"]
)


@router.get("/", response_model=list[AttachmentResponse])
async def get_attachments(db: AsyncSession = Depends(get_db)):
    statement = select(Attachment)
    result = await db.execute(statement)

    return result.scalars().all()


@router.get("/{attachment_id}", response_model=AttachmentResponse)
async def get_attachment(attachment_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Attachment).where(Attachment.id == attachment_id)
    result = await db.execute(statement)
    attachment = result.scalar_one_or_none()

    if attachment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )

    return attachment


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AttachmentResponse)
async def create_attachment(data: AttachmentCreate, db: AsyncSession = Depends(get_db)):
    attachment = Attachment(
        note_id=data.note_id,
        filename=data.filename,
        file_path=data.file_path
    )

    db.add(attachment)

    await db.commit()
    await db.refresh(attachment)

    return attachment


@router.put("/{attachment_id}", response_model=AttachmentResponse)
async def update_attachment(attachment_id: int, data: AttachmentUpdate, db: AsyncSession = Depends(get_db)):
    statement = select(Attachment).where(Attachment.id == attachment_id)
    result = await db.execute(statement)
    attachment = result.scalar_one_or_none()

    if attachment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )

    if data.filename is not None:
        attachment.filename = data.filename

    if data.file_path is not None:
        attachment.file_path = data.file_path

    await db.commit()
    await db.refresh(attachment)

    return attachment


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(attachment_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(Attachment).where(Attachment.id == attachment_id)
    result = await db.execute(statement)
    attachment = result.scalar_one_or_none()

    if attachment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )

    await db.delete(attachment)
    await db.commit()