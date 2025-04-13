from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from app.tasks import generate_video_task

# Load environment variables
REDIS_URL = os.getenv("REDIS_URL")
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

# Serve static video files
app.mount("/videos", StaticFiles(directory=VIDEO_OUTPUT), name="videos")

# Request model
class VideoRequest(BaseModel):
    prompt: str
    video_type: str  # "short" or "long"

# Root route
@app.get("/")
def root():
    return {"message": "AIKLMP backend is running 🎥"}

# Endpoint to trigger video generation
@app.post("/generate/")
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    video_id = generate_video_task.delay(request.prompt, request.video_type)
    return {
        "message": "Video generation started",
        "task_id": str(video_id),
        "status_check_url": f"/status/{video_id}"
    }

# Status check (mock/simple version — optional)
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    return {
        "task_id": task_id,
        "status": "running or completed (mock)"
    }
