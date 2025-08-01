import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

OPENAI_API_KEY = os.getenv("LLM_OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_API_BASE")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_BASE_URL = os.getenv("AZURE_API_BASE")
METADATA_LOCATION = os.getenv("METADATA_LOCATION")
AZML_SECRET_KEY = os.getenv("AZML_SECRET_KEY")
AZML_ALGORITHM = os.getenv("AZML_ALGORITHM")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGDATABASE = os.getenv("PGDATABASE")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")
WREN_UI_ENDPOINT = os.getenv("WREN_UI_ENDPOINT")
CACHE_DB = os.getenv("CACHE_DB")
MCKID_JWKS_URI = os.getenv("MCKID_JWKS_URI")
MCKID_TOKEN_ISSUER = os.getenv("MCKID_TOKEN_ISSUER")