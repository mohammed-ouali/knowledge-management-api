from pydantic import BaseModel

class CreateUser(BaseModel):
    name : str
    email : str

class UpdateUser(BaseModel):
    name : str
    email : str

class UserResponse(BaseModel):
    id : int
    name : str
    email : str