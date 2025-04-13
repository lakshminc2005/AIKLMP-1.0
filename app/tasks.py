from celery import Celery
from moviepy.editor import *  # For video generation
from PIL import Image  # For image manipulation
import os
import time

# Initialize Celery
app = Celery('tasks', broker='redis://localhost:6379/0')  # Redis as the message broker

# Path for saving the generated video
GENERATED_VIDEO_PATH = "generated_videos/"

# Ensure the folder exists
os.makedirs(GENERATED_VIDEO_PATH, exist_ok=True)

@app.task
def generate_video(prompt: str, video_type: str):
    """
    This task simulates video creation. It generates a video based on the prompt and video_type.
    """
    # Simulate processing time
    time.sleep(10)  # Simulate video generation time
    
    # Example: Generate a video with the given prompt as text on the screen
    video_path = os.path.join(GENERATED_VIDEO_PATH, f"{prompt.replace(' ', '_')}_{video_type}.mp4")
    
    # Here we create a simple video using MoviePy
    text_clip = TextClip(prompt, fontsize=70, color='white')
    text_clip = text_clip.set_pos('center').set_duration(7 * 60)  # 7 minutes long video
    video_clip = text_clip.on_color(size=(1920, 1080), color=(0, 0, 0), col_opacity=0.6)
    video_clip.write_videofile(video_path, codec="libx264")
    
    # Return the path of the generated video
    return video_path
