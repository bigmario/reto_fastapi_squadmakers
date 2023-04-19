import os
import json
import requests
from typing import List
from beanie import PydanticObjectId
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate

from api.jokes.schemas.jokes import Joke


class JokeService:
    def fetch_joke(self, url):
        joke = requests.get(url)
        serialized_joke = json.loads(joke.text)
        return JSONResponse(
            {"joke": serialized_joke},
            status_code=status.HTTP_200_OK,
        )

    async def get_jokes(self, joke_type: str):
        if joke_type == "Chuck":
            return self.fetch_joke("https://api.chucknorris.io/jokes/random")
        elif joke_type == "Dad":
            return self.fetch_joke("https://icanhazdadjoke.com/")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='El chiste debe ser de tipo "Chuck" o "Dad"',
            )
