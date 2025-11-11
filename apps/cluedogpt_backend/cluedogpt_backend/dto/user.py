from pydantic import BaseModel


class UserJwt(BaseModel):
    user_id: str
    name: str
    exp: float | None = None  # Expiration time (epoch)
    iat: float | None = None  # Issued at time (epoch)
    iss: str | None = None  # Issuer
    type: str | None = None  # Token type (e.g., "access", "refresh")
