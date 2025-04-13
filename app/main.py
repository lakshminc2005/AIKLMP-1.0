from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from app.tasks import generate_video  # Make sure tasks.py is correctly placed under /app

# Environment variables
VIDEO_OUTPUT = os.getenv("VIDEO_OUTPUT", "generated_videos")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

# Ensure the video output directory exists
os.makedirs(VIDEO_OUTPUT, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="AIKLMP - AI Video Generator")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static videos
app.mount("/videos", StaticFiles(directory=VIDEO_OUTPUT), name="videos")

# Pydantic request model
class VideoRequest(BaseModel):
    prompt: str
    video_type: str  # e.g., "short" or "long"

# Health check endpoint
@app.get("/")
def root():
    return {"message": "AIKLMP backend is live 🎥"}

# Endpoint to generate video
@app.post("/generate/")
async def generate_video_api(request: VideoRequest, background_tasks: BackgroundTasks):
    output_path = os.path.join(VIDEO_OUTPUT, f"{request.video_type}_video.mp4")
    background_tasks.add_task(generate_video, request.prompt, request.video_type, output_path)
    return {
        "message": "Video generation started in the background",
        "video_url": f"/videos/{request.video_type}_video.mp4"
    }

# Mock status endpoint (optional)
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    return {
        "task_id": task_id,
        "status": "running or completed (mock)"
    }
