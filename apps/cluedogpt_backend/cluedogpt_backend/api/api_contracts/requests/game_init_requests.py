from pydantic import BaseModel


class GameInitIterationRequest(BaseModel):
    """Request received to iterate over the creation of a game"""
    game_id: str | None = None
    message: str
    title: str