from datetime import UTC, datetime, timedelta

from ai.agents import run_story_creation_agent
from api.api_contracts.requests.game_init_requests import GameInitIterationRequest
from app_logging import logger
from models.postgres_models import Game


class GameInitService:
    async def iterate_game_init(self, game_iteration: GameInitIterationRequest):
        game = None
        if game_iteration.game_id:
            logger.info(f"Continuing game {game_iteration.game_id}")

            game = await Game.get(id=game_iteration.game_id)

            # TODO Check game owner against request user
        else:
            logger.info("Starting new game initialization")
            # TODO add owner when auth is implemented
            game = await Game.create(
                name=game_iteration.title,
                expiry_date=datetime.now(UTC) + timedelta(days=7),
            )

        await run_story_creation_agent(game, game_iteration.message)
