from ai.deps import GameAgentDeps
from ai.tools import create_story
from models.postgres_models import Game
from pydantic_ai import Agent, AgentRunResult, Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from cluedogpt_backend.ai.prompts import GAME_DESCRIPTION, STORY_CREATOR
from cluedogpt_backend.settings import settings


model = OpenAIChatModel(
    model_name=settings().ai_model_name,
    provider=OpenAIProvider(
        base_url=settings().ai_provider_base_url,
        api_key=settings().ai_model_api_key,
    ),
)


story_creation_agent = Agent(
    model=model,
    tools=[
        Tool(
            function=create_story,
            description="Create a story",
            takes_ctx=True,
        ),
    ],
    system_prompt=STORY_CREATOR.format(game_description=GAME_DESCRIPTION),
    deps_type=GameAgentDeps,
)

async def run_story_creation_agent(game: Game, message: str) -> AgentRunResult:
    deps = GameAgentDeps(game=game)

    user_prompt = f"Create or update the story with the following feedback from the user: {message}"

    if game.story:
        user_prompt += f"\n\nCurrent story: {game.story}"

    return await story_creation_agent.run(user_prompt=user_prompt, deps=deps)
