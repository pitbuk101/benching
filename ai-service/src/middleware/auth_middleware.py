import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.utility.jwt_validator import JWTTokenVerifier
from src.utility.base_jwt_validator import BaseJWTTokenVerifier
logger = logging.getLogger("wren-ai-service")

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for JWT token authentication.
    """
    async def dispatch(self, request: Request, call_next):
        """
        Intercept incoming requests and authenticate JWT tokens.

        Args:
            request (Request): The incoming request object.
            call_next (function): The function to call to proceed with
            the request handling.

        Returns:
            Response: The response object.

        Raises:
            HTTPException: If authentication fails or token is missing.
        """
        if request.url.path in ("/v1/asks"):
            logger.debug(f"Headers: {request.headers}")
            logger.debug(f"Route: {request.url.path}")
            
            # Check for Authorization header and handle token verification
            return await self.handle_authentication(request, call_next)
        
        return await call_next(request)

    async def handle_authentication(self, request: Request, call_next):
        """
        Handle the authentication process, including verification of the token.

        Args:
            request (Request): The incoming request object.
            call_next (function): The function to call to proceed with the request handling.

        Returns:
            Response: The response object.
        """
        if not self.has_authorization_header(request):
            return self.create_error_response("Authorization header is missing")
        
        token = self.extract_token(request)
        if not token:
            return self.create_error_response("Authorization token should start with Bearer")
        
        verification_result = self.verify_token(request, token)
        if not verification_result["is_authorised"]:
            return self.create_error_response(verification_result["error"])
        
        self.log_authorization(request, verification_result)
        return await call_next(request)

    def has_authorization_header(self, request: Request) -> bool:
        """
        Check if the request contains an Authorization header.

        Args:
            request (Request): The incoming request object.

        Returns:
            bool: True if the Authorization header is present, False otherwise.
        """
        return "authorization" in request.headers

    def extract_token(self, request: Request) -> str:
        """
        Extract the token from the Authorization header.

        Args:
            request (Request): The incoming request object.

        Returns:
            str: The token if valid, or None if invalid.
        """
        token = request.headers.get("authorization")
        if token and token.startswith("Bearer "):
            return token.split("Bearer ")[-1]
        raise ValueError("Authorization token is missing or invalid.")

    def verify_token(self, request: Request, token: str) -> dict:
        """
        Verify the JWT token.

        Args:
            request (Request): The incoming request object.
            token (str): The JWT token to verify.

        Returns:
            dict: The result of the verification, including 'is_authorised' and 'error' (if any).
        """
        if request.headers.get("service") == "api-bridge-service":
            logger.info("Verifying token for api-bridge-service")
            return BaseJWTTokenVerifier.verify_token(token)
        else:
            return JWTTokenVerifier.verify_token(token)

    def log_authorization(self, request: Request, verification_result: dict):
        """
        Log the authorization result.

        Args:
            request (Request): The incoming request object.
            verification_result (dict): The result of the token verification.
        """
        if request.headers.get("service") == "api-bridge-service":
            logger.info(f"User {verification_result['payload']['user']} is authorised")
        else:
            logger.info(f"User {verification_result['context']['email']} is authorised")

    def create_error_response(self, detail: str) -> JSONResponse:
        """
        Create a JSON error response.

        Args:
            detail (str): The error message to include in the response.

        Returns:
            JSONResponse: The error response.
        """
        logger.exception(detail)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": detail})
