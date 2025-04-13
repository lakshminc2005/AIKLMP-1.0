from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()  # Make sure your .env file is in the same directory

# Get Redis connection details
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"  # Redis URL for Celery

# You can add more configurations for database, video file paths, etc.
