from ai.deps import GameAgentDeps
from pydantic_ai import RunContext

from dto.game_solution import GameSolution


async def create_story(ctx: RunContext[GameAgentDeps], story: str) -> str:
    game = ctx.deps.game
    game.story = story
    await game.save()

    return "Story created successfully."


async def create_solution(ctx: RunContext[GameAgentDeps], solution: GameSolution) -> str:
    game = ctx.deps.game
    game.culprit = solution.culprit
    game.weapon = solution.weapon
    game.motive = solution.motive
    await game.save()

    return "Solution created successfully."
