from datetime import UTC, datetime, timedelta
from typing import Any, Dict

import jwt
from passlib.context import CryptContext

from cluedogpt_backend.dto.user import UserJwt, UserJwtWithTokenProperties
from cluedogpt_backend.settings import settings


# Password hashing context (reusing from user_model)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: UserJwt, expires_delta: timedelta | None = None) -> tuple[str, UserJwtWithTokenProperties]:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings().jwt_access_token_expire_minutes)

    token_type = "access"
    iat = int(datetime.now(UTC).timestamp())
    exp = int(expire.timestamp())
    iss = "cluedogpt"

    user_jwt_with_props = UserJwtWithTokenProperties(
        user_id=data.user_id,
        name=data.name,
        exp=exp,
        iat=iat,
        iss=iss,
        type=token_type,
    )

    encoded_jwt = jwt.encode(user_jwt_with_props.model_dump(), settings().jwt_secret_key, algorithm=settings().jwt_algorithm)
    return encoded_jwt, user_jwt_with_props


def create_refresh_token(data: UserJwt, expires_delta: timedelta | None = None) -> tuple[str, UserJwtWithTokenProperties]:
    """Create a JWT refresh token."""
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=settings().jwt_refresh_token_expire_days)

    exp = int(expire.timestamp())
    token_type = "refresh"
    iat = int(datetime.now(UTC).timestamp())
    iss = "cluedogpt"

    user_jwt_with_props = UserJwtWithTokenProperties(
        user_id=data.user_id,
        name=data.name,
        exp=exp,
        iat=iat,
        iss=iss,
        type=token_type,
    )

    encoded_jwt = jwt.encode(user_jwt_with_props.model_dump(), settings().jwt_secret_key, algorithm=settings().jwt_algorithm)
    return encoded_jwt, user_jwt_with_props


def verify_token(token: str, token_type: str = "access") -> Dict[str, Any] | None:  # noqa: S107
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, settings().jwt_secret_key, algorithms=[settings().jwt_algorithm])

        # Check if the token type matches
        if payload.get("type") != token_type:
            return None

        return payload
    except jwt.PyJWTError:
        return None
