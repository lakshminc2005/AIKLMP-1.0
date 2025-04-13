from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from app.tasks import generate_video 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AIKLMP is running 🎥"}
# Import the new video generation function

# Environment variables for setup
VIDEO_OUTPUT = os.getenv("VIDEO_OUTPUT", "generated_videos")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

# FastAPI app initialization
app = FastAPI(title="AIKLMP - AI Video Generator")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated videos as static files
app.mount("/videos", StaticFiles(directory=VIDEO_OUTPUT), name="videos")

# Request model for video generation
class VideoRequest(BaseModel):
    prompt: str
    video_type: str  # "short" or "long"

# Root endpoint
@app.get("/")
def root():
    return {"message": "AIKLMP backend is live 🎥"}

# Endpoint to trigger video generation
@app.post("/generate/")
async def generate_video_api(request: VideoRequest, background_tasks: BackgroundTasks):
    # File path for saving the generated video
    output_path = os.path.join(VIDEO_OUTPUT, f"{request.video_type}_video.mp4")
    # Add task to background execution
    background_tasks.add_task(generate_video, request.prompt, request.video_type, output_path)
    return {
        "message": "Video generation started in the background",
        "video_url": f"/videos/{request.video_type}_video.mp4"
    }

# Optional: Endpoint to check video generation status (mock)
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    return {
        "task_id": task_id,
        "status": "running or completed (mock)"
    }
