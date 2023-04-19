import requests
from beanie import PydanticObjectId
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from api.jokes.schemas.jokes import Joke


class JokeService:
    def __fetch_joke(self, url):
        headers = {"Accept": "application/json"}
        joke = requests.get(url, headers=headers)
        return joke.json()

    async def get_jokes(self, joke_type: str):
        if joke_type == "Chuck":
            joke = self.__fetch_joke("https://api.chucknorris.io/jokes/random")
            return JSONResponse(
                {"joke": joke["value"]},
                status_code=status.HTTP_200_OK,
            )

        elif joke_type == "Dad":
            joke = self.__fetch_joke("https://icanhazdadjoke.com")
            return JSONResponse(
                {"joke": joke["joke"]},
                status_code=status.HTTP_200_OK,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='El chiste debe ser de tipo "Chuck" o "Dad"',
            )

    async def save_joke(self, body: Joke = Body(...)):
        existing_joke = await Joke.find_one(Joke.joke == body.joke)

        if not existing_joke:
            new_joke = await body.create()
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

    async def update_joke(self, id: PydanticObjectId, body: Joke = Body(...)):
        update_joke = await Joke.find_one(Joke.id == id)
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
