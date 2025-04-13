from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

from app.tasks import generate_video  # Make sure app/tasks.py exists with generate_video()

# Environment variables
VIDEO_OUTPUT = os.getenv("VIDEO_OUTPUT", "generated_videos")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

# Ensure video output directory exists
os.makedirs(VIDEO_OUTPUT, exist_ok=True)

# FastAPI app
app = FastAPI(title="AIKLMP - AI Video Generator")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, Videos)
app.mount("/static", StaticFiles(directory="static/css"), name="static/css")
app.mount("/videos", StaticFiles(directory=VIDEO_OUTPUT), name="videos")

# Set up Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="templates")

# Pydantic model
class VideoRequest(BaseModel):
    prompt: str
    video_type: str  # "short" or "long"

# Render frontend page
@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Video generation API
@app.post("/generate/")
async def generate_video_api(request: VideoRequest, background_tasks: BackgroundTasks):
    output_path = os.path.join(VIDEO_OUTPUT, f"{request.video_type}_video.mp4")
    background_tasks.add_task(generate_video, request.prompt, request.video_type, output_path)
    return {
        "message": "Video generation started in the background",
        "video_url": f"/videos/{request.video_type}_video.mp4"
    }

# (Optional) Mock task status
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    return {
        "task_id": task_id,
        "status": "running or completed (mock)"
    }
