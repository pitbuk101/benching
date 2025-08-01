import requests
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from fastapi import HTTPException
from typing import Dict, Any
from src.env import MCKID_JWKS_URI, MCKID_TOKEN_ISSUER

from jose import jwk

class JWKSClient:
    def __init__(self, jwks_uri: str):
        self.jwks_uri = jwks_uri
        self._keys = None

    def get_signing_key(self, kid: str):
        if self._keys is None:
            response = requests.get(self.jwks_uri)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Unable to fetch JWKS")
            self._keys = response.json().get("keys", [])
        for key in self._keys:
            if key["kid"] == kid:
                # Use jose.jwk.construct to build the public key object
                return jwk.construct(key)
        raise HTTPException(status_code=401, detail="Invalid token: signing key not found")

class JWTTokenVerifier:
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        try:
            unverified_header = jwt.get_unverified_header(token)
            jwks_client = JWKSClient(MCKID_JWKS_URI)
            key = jwks_client.get_signing_key(unverified_header["kid"])

            payload = jwt.decode(
                token,
                key=key,
                algorithms=["RS256"],
                issuer=MCKID_TOKEN_ISSUER,
                options={"verify_aud": False},
            )

            if "preferred_username" not in payload or "email" not in payload:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            return {
                "valid": True,
                "email": payload["email"],
                "preferred_username": payload["preferred_username"],
                **payload
            }

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Token validation error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        
