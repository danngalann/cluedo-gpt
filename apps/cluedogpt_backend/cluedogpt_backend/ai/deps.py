from dataclasses import dataclass

from models.postgres_models import Game


@dataclass
class GameAgentDeps:
    game: Game
