from tortoise import Tortoise

from cluedogpt_backend.settings import settings


TORTOISE_ORM = {
    "connections": {
        "default": settings.postgres_dsn,
    },
    "apps": {
        "models": {
            "models": ["cluedogpt_backend.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "UTC",
}


async def init_db() -> None:
    """Initialize the Tortoise ORM with the shared models."""
    await Tortoise.init(config=TORTOISE_ORM)


async def generate_schemas() -> None:
    """Generate database schemas."""
    await init_db()
    await Tortoise.generate_schemas()


async def close_connections() -> None:
    """Close database connections."""
    await Tortoise.close_connections()
