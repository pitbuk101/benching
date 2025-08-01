from src.env import AZML_SECRET_KEY, AZML_ALGORITHM
from datetime import datetime, timedelta, timezone
import jwt
from src.utils.logs import get_custom_logger
logger = get_custom_logger(__name__)
def generate_jwt() -> str:
    payload = {
        "user": "AZ_ML_ENDPOINT",  # Issuer
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=30),  # Expiry
    }
    token = jwt.encode(payload, AZML_SECRET_KEY, algorithm=AZML_ALGORITHM)
    return token