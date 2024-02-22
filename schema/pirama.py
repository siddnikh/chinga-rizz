from pydantic import BaseModel
from anthropos import User

class Project(BaseModel):
    owner: User
    title: str
    additional_context: bool
    context: str
    slide_count: int
    color_scheme: int
    is_deleted: bool

class ColorScheme(BaseModel):
    primary_color: str
    secondary_color: str
    accent_color: str

class Slide(BaseModel):
    project: Project
    title: str
    content: str
    color_scheme: ColorScheme
    slide_number: int
    is_deleted: bool