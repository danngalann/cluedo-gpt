"""
Sample API router for items.
This demonstrates basic FastAPI endpoint creation with common HTTP methods.
"""

from typing import List

from apps.cluedogpt_backend.cluedogpt_backend.models.postgres_models import Item, ItemPydantic
from fastapi import APIRouter, HTTPException, status


# Create a router for items
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}},
)


@router.get("/", response_model=List[ItemPydantic])
async def get_items():
    """
    Get all items.
    """

    # Direct database access without repository pattern

    items = await Item.all()
    return await ItemPydantic.from_queryset(items)


@router.get("/{item_id}", response_model=ItemPydantic)
async def get_item(item_id: str):
    """
    Get a single item by ID.
    """

    # Direct database access without repository pattern

    item = await Item.get_or_none(id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return await ItemPydantic.from_tortoise_orm(item)


@router.post("/", response_model=ItemPydantic, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemPydantic):
    """
    Create a new item.
    """

    # Direct database access without repository pattern

    new_item = await Item.create(**item.dict())
    return await ItemPydantic.from_tortoise_orm(new_item)
