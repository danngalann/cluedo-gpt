from api.api_contracts.requests.auth_requests import SignUpRequest
from api.api_contracts.responses.auth_response import SignUpResponse
from auth.jwt_auth import create_access_token, create_refresh_token
from dto.user import UserJwt
from fastapi import APIRouter, Response
from models.postgres_models import Player


# Create a router for items
router = APIRouter(
    prefix="/auth",
    tags=["Game Initialization"],
)


@router.post("/sign-up", response_model=SignUpResponse)
async def sign_up(request: SignUpRequest, response: Response):
    player = await Player.create(
        name=request.username,
    )

    user_jwt = UserJwt(
        name=player.name,
        user_id=str(player.id),
    )

    access_token, access_token_user = create_access_token(user_jwt)
    refresh_token, refresh_token_user = create_refresh_token(user_jwt)

    # Calculate max_age for cookie (seconds until expiry)
    max_age = int(refresh_token_user.exp - refresh_token_user.iat)

    # Set refresh token as httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=max_age,
        httponly=True,
        secure=True,  # Use secure cookies in production
        samesite="strict",
    )

    return SignUpResponse(
        access_token=access_token,
        access_token_expires_at=access_token_user.exp,
    )
