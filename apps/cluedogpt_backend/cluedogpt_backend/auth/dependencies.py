from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from starlette import status

from cluedogpt_backend.api.exceptions import BadRequestError
from cluedogpt_backend.auth.jwt_auth import verify_token
from cluedogpt_backend.dto.user import UserJwt


# Security schemes
jwt_bearer = HTTPBearer(auto_error=False)


async def get_current_user_from_jwt(
    request: Request,
    token: HTTPAuthorizationCredentials | None = Security(jwt_bearer),
) -> UserJwt:
    """Get current user from access_token cookie"""
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the token
    payload = verify_token(access_token, "access")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")

    if not user_id:
        raise BadRequestError(
            error_code="invalid_token",
            message="Invalid token payload",
        )

    user = UserJwt(**payload)

    return user


async def authenticate_user(
    request: Request,
    user: UserJwt | None = Depends(get_current_user_from_jwt),
) -> str | UserJwt:
    """
    Authenticate using JWT token.
    Returns UserJwt object if authenticated via JWT.
    """

    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_refresh_token_from_cookie(request: Request) -> str | None:
    """Extract refresh token from secure cookie."""
    return request.cookies.get("refresh_token")
