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
    path="/joke/{joke_type}",
    status_code=status.HTTP_200_OK,
    summary="Get a joke from https://api.chucknorris.io/ or https://icanhazdadjoke.com/api",
)
async def get_joke(
    joke_type: str = Path(...),
    subscription_service: JokeService = Depends(),
):
    return await subscription_service.get_jokes(joke_type)


########################
# Save Joke on DB
########################
@jokes_router.post(
    path="/joke",
    status_code=status.HTTP_201_CREATED,
    summary="Save a Joke on Database",
)
async def save_joke(
    body: Joke = Body(...),
    joke_service: JokeService = Depends(),
):
    """
    Save Joke:
    """
    return await joke_service.save_joke(body)


########################
# GET ALL JOKES ON DB
########################
@jokes_router.get(
    path="/jokes",
    status_code=status.HTTP_200_OK,
    summary="Get All Jokes from Database",
    response_model=Page[Joke],
    response_model_exclude_unset=True,
)
async def get_all_jokes(
    subscription_service: JokeService = Depends(),
) -> Page[Joke]:
    try:
        subscriptions = await subscription_service.get_all_jokes()
        return paginate(subscriptions)
    except Exception as e:
        return f"An exception occurred: {e}"


########################
# UPDATE Joke on DB
########################
@jokes_router.patch(
    path="/joke/{id}",
    status_code=status.HTTP_200_OK,
    summary="Update a Joke on Database",
)
async def update_joke(
    number: PydanticObjectId = Path(...),
    body: Joke = Body(...),
    joke_service: JokeService = Depends(),
):
    """
    UPdate Joke:
    """
    return await joke_service.update_joke(number, body)


#############################
# DELETE JOKE FROM DB BY ID
#############################
@jokes_router.delete(
    path="/joke/{number}",
    status_code=status.HTTP_200_OK,
    summary="Delete One Joke By Number",
    response_model_exclude_unset=True,
)
async def delete_joke(
    number: PydanticObjectId = Path(...),
    joke_service: JokeService = Depends(),
) -> dict:
    try:
        return await joke_service.delete_joke(number)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Joke not found!"
        )
