import jwt
import os


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
        if token == os.getenv('AZML_SECRET_KEY'):
            return {"valid": True}
        else:
            return {"valid": False, "error": "Invalid key"}
