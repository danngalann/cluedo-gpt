
from api.api_contracts.requests.game_init_requests import GameInitIterationRequest
from fastapi import APIRouter, Depends
from services.game_init_service import GameInitService


# Create a router for items
router = APIRouter(
    prefix="/game-init",
    tags=["Game Initialization"],
)


@router.post("/iteration")
async def iteration(request: GameInitIterationRequest, service: GameInitService = Depends(GameInitService)):
    return service.iterate_game_init(request)
