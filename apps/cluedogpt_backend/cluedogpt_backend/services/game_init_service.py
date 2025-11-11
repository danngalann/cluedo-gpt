from datetime import UTC, datetime, timedelta

from api.api_contracts.requests.game_init_requests import GameInitIterationRequest
from app_logging import logger
from models.postgres_models import Game


class GameInitService:
    def iterate_game_init(self, game_iteration: GameInitIterationRequest):
        game = None
        if game_iteration.game_id:
            logger.info(f"Continuing game {game_iteration.game_id}")

            game = Game.get(id=game_iteration.game_id)

            # TODO Check game owner against request user
        else:
            logger.info("Starting new game initialization")
            # TODO add owner when auth is implemented
            game = Game.create(
                name=game_iteration.title,
                expiry_date=datetime.now(UTC) + timedelta(days=7),
            )

        # TODO Pass the message to the LLM and get a response
        # The response may contain a story, culprit, weapon, motive, etc.
