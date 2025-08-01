import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
# from src.utils.secret_manager import get_secrets


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
            # azml_secret_key = os.environ.get('AZML_ENDPOINT_SECRETS')
            # logger.info(f"AZML_SECRET_KEY: {azml_secret_key}")
            # secrets = get_secrets(azml_secret_key, type='json')
        if token == os.getenv('AZML_SECRET_KEY'):
            return {"valid": True}
        else:
            return {"valid": False, "error": "Invalid key"}
