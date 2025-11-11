from pydantic import BaseModel


class UserJwt(BaseModel):
    user_id: str
    name: str


class UserJwtWithTokenProperties(UserJwt):
    exp: float  # Expiration time (epoch)
    iat: float  # Issued at time (epoch)
    iss: str  # Issuer
    type: str  # Token type (e.g., "access", "refresh")
