from typing import List
from fastapi import HTTPException, status


class MathService:
    async def get_lcm(self, numbers: str):
        try:
            # cast string to list of integers
            numbers = [int(number) for number in list(numbers.split(","))]

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
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="List must contain only integers and be separated by commas (,)",
            )

    async def plus_one(self, number: int):
        return {"result": number + 1}
