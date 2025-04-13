from pydantic import BaseModel
from typing import Optional

# Model to represent video generation request
class VideoGenerationRequest(BaseModel):
    prompt: str
    video_type: str
    status: Optional[str] = "Pending"  # Default status when the task is started
