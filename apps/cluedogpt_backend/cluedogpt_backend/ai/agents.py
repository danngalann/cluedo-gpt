from ai.deps import AgentDepedencies
from ai.tools import create_game
from pydantic_ai import Agent, Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from cluedogpt_backend.settings import settings


model = OpenAIChatModel(
    model_name=settings.ai_model_name,
    provider=OpenAIProvider(
        base_url=settings.ai_provider_base_url,
        api_key=settings.ai_model_api_key,
    ),
)

action_planner_agent = Agent(
    model=model,
    tools=[
        Tool(
            function=create_game,
            description="Create a game",
            takes_ctx=True,
        ),
    ],
    system_prompt="TODO",
    deps_type=AgentDepedencies,
)
