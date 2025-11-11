from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cluedogpt_backend.api.routers import items
from cluedogpt_backend.app_logging import initialize_logging_from_settings
from cluedogpt_backend.infrastructure.postgres_db import init_db
from cluedogpt_backend.settings import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize_logging_from_settings()

    # Initialize databases on startup
    await init_db()

    yield

    # Clean up resources on shutdown

    # Postgres cleanup will be handled by Tortoise ORM automatically


# Create FastAPI app with hardcoded branding
app = FastAPI(
    title="Cluedogpt Backend API",
    description="API for Cluedogpt Backend",
    version="1.0.0",
    # Only enable Swagger/ReDoc if documentation is enabled
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url="/redoc" if settings.enable_docs else None,
    lifespan=lifespan,
    # Add additional branding in the API metadata
    openapi_tags=[
        {
            "name": "Cluedogpt Backend",
            "description": "Cluedogpt Backend API documentation",
        },
    ],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include routers
app.include_router(items, prefix="/api/v1", tags=["items"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
