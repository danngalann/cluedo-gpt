"""
PostgreSQL database initialization module using Tortoise ORM.
"""

from tortoise import Tortoise

from cluedogpt_backend.settings import settings


async def init_postgres_db():
    """
    Initialize the PostgreSQL database connection using Tortoise ORM.
    This is designed to be called during the FastAPI application startup.
    """
    await Tortoise.init(
        db_url=settings.postgres_dsn,
        modules={
            "models": [
                # List your document models here. For example:
                # "cluedogpt_backend.models.user.User",
                # "cluedogpt_backend.models.item.Item",
            ],
        },
    )

    # Generate schemas for all models
    await Tortoise.generate_schemas()

    return Tortoise
