from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from middleware.auth import JWTTokenVerifier
from ada.utils.logs.logger import get_logger

logger = get_logger("unified-ml-endpoint authentication")

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
        # bypass the health check route
        if request.url.path == "/health":
            return await call_next(request)

        if "authorization" not in request.headers:
            logger.error(f"Authorization header missing, route: {request.url.path}", exc_info=True)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Authorization header is missing"})
        # Extract token from Authorization header
        token = request.headers.get("authorization")
        if token.startswith("Bearer "):
            token = token.split("Bearer ")[-1]
            # Verify token
            verification_result = JWTTokenVerifier.verify_token(token)
            if not verification_result["valid"]:
                logger.error(f"verification_result: {verification_result} : , route: {request.url.path}", exc_info=True)
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": verification_result["error"]})
            else:
                logger.info("Token verified successfully")
                response = await call_next(request)
                return response
        else:
            logger.error(f"Bearer keyword missing, route: {request.url.path}", exc_info=True)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Authorization token should start with Bearer"})