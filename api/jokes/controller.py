from typing import List, Any
from beanie import PydanticObjectId
from fastapi import (
    APIRouter,
    Header,
    Body,
    status,
    Path,
    HTTPException,
    Depends,
)
from fastapi_pagination import Page, paginate

from .schemas.jokes import Joke
from .service.joke_service import JokeService

from config import Settings

conf = Settings()

########################
# Jokes Router
########################
jokes_router = APIRouter(tags=["Jokes"])

#################################################################################
# GET JOKES FROM https://api.chucknorris.io/ or https://icanhazdadjoke.com/api
#################################################################################
@jokes_router.get(
    path="/chiste/{joke_type}",
    status_code=status.HTTP_200_OK,
    summary="Get Jokes",
)
async def get_joke(
    joke_type: str = Path(...),
    subscription_service: JokeService = Depends(),
):
    try:
        return await subscription_service.get_jokes(joke_type)
    except Exception as e:
        return f"An exception occurred: {e}"
