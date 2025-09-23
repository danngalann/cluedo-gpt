from cluedogpt_backend.api.routers.items import router as items_router


# Export routers - this makes it possible to import them from the routers package directly
items = items_router
