import random
import requests
from beanie import PydanticObjectId
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from api.jokes.schemas import Joke


class JokeService:
    def __fetch_joke(self, url):
        headers = {"Accept": "application/json"}
        joke = requests.get(url, headers=headers)
        return joke.json()

    async def get_jokes(self, joke_type: str):
        try:
            joke_type = joke_type.lower()
            print(joke_type)
            if joke_type == "chuck":
                joke = self.__fetch_joke("https://api.chucknorris.io/jokes/random")
                return JSONResponse(
                    {"joke": joke["value"]},
                    status_code=status.HTTP_200_OK,
                )
            elif joke_type == "dad":
                joke = self.__fetch_joke("https://icanhazdadjoke.com")
                return JSONResponse(
                    {"joke": joke["joke"]},
                    status_code=status.HTTP_200_OK,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Joke type must be "Chuck" o "Dad"',
                )
        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Joke server is taking too much time to respond",
            )

    async def get_random_joke(self):
        try:
            joke_sources = [
                "https://api.chucknorris.io/jokes/random",
                "https://icanhazdadjoke.com",
            ]
            joke = self.__fetch_joke(random.choice(joke_sources))
            if "value" in joke:
                return JSONResponse(
                    {"joke": joke["value"]},
                    status_code=status.HTTP_200_OK,
                )
            else:
                return JSONResponse(
                    {"joke": joke["joke"]},
                    status_code=status.HTTP_200_OK,
                )
        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="Joke server is taking too much time to respond",
            )

    async def save_joke(self, body: Joke = Body(...)):
        existing_joke = await Joke.find_one(Joke.joke == body.joke)

        if not existing_joke:
            await body.create()
            return JSONResponse(
                {"Message": "Joke successfully stored"},
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                {"Message": "This joke is already registered"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    async def get_all_jokes(self) -> Page[Joke]:
        return await Joke.find_all().to_list()

    async def update_joke(self, number: PydanticObjectId, body: Joke = Body(...)):
        update_joke = await Joke.get(number)
        if update_joke:
            update_joke.joke = body.joke
            await update_joke.save()
            return JSONResponse(
                {"Message": "Joke successfully updated"},
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                {"Message": "ID not registered!!"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    async def delete_joke(self, id: PydanticObjectId) -> dict:
        joke = await Joke.get(id)
        await joke.delete()
        return {"message": "Joke successfully deleted"}
