from ai.deps import GameAgentDeps
from pydantic_ai import RunContext


async def create_story(ctx: RunContext[GameAgentDeps], story: str) -> str:
    game = ctx.deps.game
    game.story = story
    await game.save()

    return "Story created successfully."


async def update_game():
    pass
