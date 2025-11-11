from pydantic import BaseModel


class SignUpResponse(BaseModel):
    access_token: str
    access_token_expires_at: float
