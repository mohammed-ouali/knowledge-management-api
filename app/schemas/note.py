from pydantic import BaseModel

class CreateNote(BaseModel):
    title : str
    content : str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str

class UpdateNote(BaseModel):
    title: str
    content: str