from pydantic import BaseModel
from anthropos import User

class Video(BaseModel):
    owner: User
    context: str
    generated_text: str
    audio_url: str
    images: list[str]
    generated_video_url: str
    is_deleted: bool