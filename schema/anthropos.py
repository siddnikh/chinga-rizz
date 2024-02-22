from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
    password: str
    is_active: bool

class UserResponse(BaseModel):
    name: str
    age: int
    email: str