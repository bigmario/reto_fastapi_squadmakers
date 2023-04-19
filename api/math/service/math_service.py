import requests
from typing import List
from beanie import PydanticObjectId
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate

from api.jokes.schemas.jokes import Joke


class MathService:
    async def get_lcm(
        self,
        numbers: List[int],
    ):
        def gcd(a: int, b: int) -> int:
            if a == 0:
                return b
            return gcd(b % a, a)

        def lcm(a: int, b: int) -> int:
            return (a * b) // gcd(a, b)

        result = numbers[0]
        for i in range(1, len(numbers)):
            result = lcm(result, numbers[i])

        return {"lcm": result}

    async def plus_one(self, number: int):
        return {"result": number + 1}
