import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# --- General ---
CLIENT_NAME = "default_run"

# --- Paths ---
BASE_TEMP_DIR = "./data/temp/"
LOG_DIR = "./logs/"

# --- S3 Configuration ---
S3_INPUT_BUCKET = os.getenv("INPUT_S3_BUCKET")
S3_BENCHMARK_INPUT_BUCKET = os.getenv("BENCHMARK_INPUT_S3_BUCKET")

# --- Snowflake Configuration ---
SNOWFLAKE_USER = os.getenv("EU_SF_USERNAME")
SNOWFLAKE_PASSWORD = os.getenv("EU_SF_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("EU_SF_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("EU_SF_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("EU_IDP_SF_DATABASE")
SNOWFLAKE_ROLE = os.getenv("EU_SF_ROLE")

# --- Postgres Configuration ---
POSTGRES_HOST = os.getenv("PGHOST")
POSTGRES_PORT = os.getenv("PGPORT")
POSTGRES_DB = os.getenv("PGDATABASE")
POSTGRES_USER = os.getenv("PGUSER")
POSTGRES_PASSWORD = os.getenv("PGPASSWORD")
POSTGRES_SCHEMA = os.getenv("PGSCHEMA")
POSTGRES_SSL_MODE = "require"

# --- LLM Configuration ---
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.0
LLM_BATCH_SIZE = 10
LLM_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_BASE_URL")
LLM_TIMEOUT_SECONDS = 120
LLM_MAX_RETRIES = 2
LLM_MAX_WORKERS_NORMALIZATION = 10

# --- Logging Configuration ---
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_ENABLED = True

# --- Input Data Configuration ---
INPUT_SOURCE_TEXT_COLUMN = [
    "Item Description",
    "Description",
    "Desc",
    "Invoice description",
    "Material"
]

# --- Normalization Stage Configuration ---
NORM_INPUT_TEXT_COLUMN_FOR_LLM = "description"
NORM_LLM_PROMPT_KEY = "generic_normalization_prompt"
NORM_LLM_OUTPUT_COLUMNS = [
    "Type",
    "Extracted Quantity",
    "Normalized Description",
    "B2B Query",
    "Attribute 1",
    "Attribute 2",
    "Attribute 3"
]
NORM_PRE_LLM_OPERATIONS = [
    {"type": "strip_column", "column": "description"},
    {"type": "clean_text_basic", "column": "description"}
]

# Add more as needed for other config keys referenced in the code 