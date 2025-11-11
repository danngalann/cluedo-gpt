from pydantic import BaseModel


class GameSolution(BaseModel):
    culprit: str
    weapon: str
    motive: str