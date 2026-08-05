from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    statement = select(User)
    result = await db.execute(statement)
    users = result.scalars().all()

    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    statement = select(User).where(User.id == user_id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    updated_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    statement = select(User).where(User.id == user_id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if updated_data.username is not None:
        user.username = updated_data.username

    if updated_data.email is not None:
        user.email = updated_data.email

    if updated_data.password is not None:
        user.password_hash = updated_data.password

    await db.commit()
    await db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    statement = select(User).where(User.id == user_id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.delete(user)

    await db.commit()