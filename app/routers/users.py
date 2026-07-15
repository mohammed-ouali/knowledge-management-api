from fastapi import APIRouter, HTTPException, status
from app.schemas.user import CreateUser, UserResponse, UpdateUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

users = []


@router.get("/", response_model=list[UserResponse])
async def get_users():
    return users


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int):
    for user in users:
        if user["id"] == id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: CreateUser):
    user = user.model_dump()
    user["id"] = len(users) + 1
    users.append(user)
    return user


@router.put("/{id}", response_model=UserResponse)
async def update_user(id: int, updated_user: UpdateUser):
    for user in users:
        if user["id"] == id:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )