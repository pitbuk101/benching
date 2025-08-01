import jwt
from jwt import PyJWKClient
import os

MCKID_JWKS_URI=os.getenv("MCKID_JWKS_URI")
MCKID_EXPECTED_AUDIENCE=os.getenv("MCKID_EXPECTED_AUDIENCE")
MCKID_TOKEN_ISSUER=os.getenv("MCKID_TOKEN_ISSUER")

class JWTTokenVerifier:
    """
    Utility class for verifying JWT tokens.
    """

    @staticmethod
    def _get_signing_key(token: str) -> str:
        """
        Retrieve the signing key from the JWKS URI.

        Args:
            token (str): JWT token string.

        Returns:
            str: The signing key extracted from JWKS.
        """
        jwks_client = PyJWKClient(MCKID_JWKS_URI)
        jwks_key = jwks_client.get_signing_key_from_jwt(token)
        return jwks_key.key

    @staticmethod
    def _get_signing_alg(token: str) -> str:
        """
        Retrieve the token signing algorithm from JWT headers.

        Args:
            token (str): JWT token string.

        Returns:
            str: The signing algorithm extracted from JWT headers.
        """
        jwt_headers = JWTTokenVerifier._get_jwt_headers(token)
        return jwt_headers["alg"]

    @staticmethod
    def _get_jwt_headers(token: str) -> dict:
        """
        Retrieve JWT token headers.

        Args:
            token (str): JWT token string.

        Returns:
            dict: The headers of the JWT token.
        """
        return jwt.get_unverified_header(token) # NOSONAR

    @staticmethod
    def _decode_token(token: str) -> dict:
        """
        Decode the JWT token and verify its signature.

        Args:
            token (str): JWT token string.

        Returns:
            dict: Contextual information extracted from the token.
        """
        signing_alg = JWTTokenVerifier._get_signing_alg(token)
        signing_key = JWTTokenVerifier._get_signing_key(token)

        token_context = jwt.decode(
            token,
            algorithms=signing_alg,
            key=signing_key,
            audience=MCKID_EXPECTED_AUDIENCE,
            issuer=MCKID_TOKEN_ISSUER,
            options={"verify_signature": True},
        )
        return token_context

    @staticmethod
    def _build_user_meta(token_context: dict) -> dict:
        """
        Build user metadata from the token context.

        Args:
            token_context (dict): The context extracted from the JWT token.

        Returns:
            dict: User metadata including email, first name,
            last name, and firm_no.

        Note:
            For user accounts (Client to Machine calls), the email
            is used to build the metadata. For service accounts
            (Machine to Machine calls), an empty dictionary is returned.
        """
        email = token_context.get("email")

        # User Account (Client to Machine calls)
        if email:
            return {
                "email": email.lower(),
                "first_name": token_context.get("given_name"),
                "last_name": token_context.get("family_name"),
                "firm_no": token_context.get("fmno"),
                "account_type": "USER",
            }
        # Service Account (Machine to Machine calls)
        else:
            # Service accounts don't have an email or firm_no
            # So we are creating unique email & fmno using clientId
            client_id = token_context.get("clientId")
            return {
                "email": f"{client_id}@sai.mckinsey.com",
                "first_name": "Service",
                "last_name": "Account",
                "firm_no": client_id,
                "account_type": "SERVICE",
            }

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
            token_context = JWTTokenVerifier._decode_token(token)
            metadata = JWTTokenVerifier._build_user_meta(token_context)
            return {"is_authorised": True, "context": metadata}
        except Exception as error:
            return {"is_authorised": False, "error": error.__str__()}