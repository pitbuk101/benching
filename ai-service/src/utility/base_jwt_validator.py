import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from src.utility.secret_manager import get_secrets
from loguru import logger


class BaseJWTTokenVerifier:
    """
    Utility class for verifying JWT tokens.
    """

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify the authenticity of the JWT token.

        Args:
            token (str): JWT token string.

        Returns:
            dict: A dictionary containing the verification result
            and token context.
        """
        try:
            # azml_secret_key = os.environ.get('AZML_ENDPOINT_SECRETS')
            # logger.info(f"AZML_SECRET_KEY: {azml_secret_key}")
            # secrets = get_secrets(azml_secret_key, type='json')
            # payload = jwt.decode(token, secrets.get("SECRET_KEY"), algorithms=[secrets.get("ALGORITHM")])
            payload = jwt.decode(token, os.environ.get("AZML_SECRET_KEY"), algorithms=[os.environ.get("AZML_ALGORITHM")])
            return {"is_authorised": True, "payload": payload}
        except ExpiredSignatureError as e:
            logger.exception(f"Token has expired: {e}")
            return {"is_authorised": False, "error": "Token has expired"}
        except InvalidTokenError as e:
            logger.exception(f"Invalid token: {e}")
            return {"is_authorised": False, "error": "Invalid token"}
