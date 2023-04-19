from typing import List
from fastapi import (
    APIRouter,
    Query,
    status,
    Depends,
)
from .service.math_service import MathService

from config import Settings

conf = Settings()

########################
# Math Router
########################
math_router = APIRouter(tags=["Math"])


@math_router.get(
    path="/lcm",
    status_code=status.HTTP_200_OK,
    summary="Calculate the least common multiple ",
)
async def get_lcm(
    numbers: List[int] = Query(
        ..., description="Enter list of integers separated by comma"
    ),
    math_service: MathService = Depends(),
):
    return await math_service.get_lcm(numbers)


@math_router.get(
    path="/plus-one",
    status_code=status.HTTP_200_OK,
    summary="Adds 1 to the input number",
)
async def plus_one(
    number: int = Query(..., description="Enter a number"),
    math_service: MathService = Depends(),
):
    return await math_service.plus_one(number)
