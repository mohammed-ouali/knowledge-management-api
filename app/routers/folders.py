from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/folders",
    tags=["Folders"]
)

folders = []


@router.get("/")
async def get_folders():
    return folders


@router.get("/{id}")
async def get_folder(id: int):
    for folder in folders:
        if folder["id"] == id:
            return folder
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Folder not found"
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_folder(folder: dict):
    folder["id"] = len(folders) + 1
    folders.append(folder)
    return folder


@router.put("/{id}")
async def update_folder(id: int, updated_folder: dict):
    for folder in folders:
        if folder["id"] == id:
            folder["name"] = updated_folder["name"]
            return folder

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Folder not found"
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(id: int):
    for folder in folders:
        if folder["id"] == id:
            folders.remove(folder)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Folder not found"
    )