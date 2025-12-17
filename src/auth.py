import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

API_TOKENS: set[str] = set()

_tokens_env = os.environ.get("API_TOKENS", "")
if _tokens_env:
    API_TOKENS = {token.strip() for token in _tokens_env.split(",") if token.strip()}

security = HTTPBearer(auto_error=False)


def verify_token(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> None:
    if not API_TOKENS:
        return

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    if not any(secrets.compare_digest(token, valid_token) for valid_token in API_TOKENS):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
