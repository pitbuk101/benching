import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
# from src.utils.secret_manager import get_secrets
from loguru import logger


class JWTTokenVerifier:
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
            payload = jwt.decode(token, os.environ.get("AZML_SECRET_KEY"), algorithms=[os.environ.get("AZML_ALGORITHM")])
            return {"valid": True, "payload": payload}
        except ExpiredSignatureError:
            return {"valid": False, "error": "Token has expired"}
        except InvalidTokenError:
            return {"valid": False, "error": "Invalid token"}
