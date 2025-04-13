from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pathlib import Path
from .tasks import generate_video  # Import Celery task
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or add specific Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


# Route to render the home page (frontend)
@app.get("/", response_class=JSONResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route to trigger video generation (POST request)
@app.post("/generate-video/")
async def generate_video_task(request: Request, prompt: str, video_type: str):
    # Start the video generation task asynchronously using Celery
    task = generate_video.apply_async(args=[prompt, video_type])
    
    # Return task ID to the frontend so the user can track progress
    return JSONResponse(content={"task_id": task.id}, status_code=202)


# Route to fetch task status (optional, you can remove it if you don't need it)
@app.get("/task-status/{task_id}", response_class=JSONResponse)
async def get_task_status(task_id: str):
    task = generate_video.AsyncResult(task_id)
    return JSONResponse(content={"status": task.status, "result": task.result})
