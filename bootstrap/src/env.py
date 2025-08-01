import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

LLM_OPENAI_API_KEY = os.getenv("LLM_OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_API_BASE")
METADATA_LOCATION = os.getenv("METADATA_LOCATION")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")
WREN_UI_ENDPOINT = os.getenv("WREN_UI_ENDPOINT")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")