from pydantic import BaseModel


class SignUpRequest(BaseModel):
    username: str
